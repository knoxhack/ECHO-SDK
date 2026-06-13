import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'
import process from 'node:process'
import { spawnSync } from 'node:child_process'

const repoRoot = process.cwd()
const script = path.join(repoRoot, 'scripts', 'stage-native-sdk-rc1-release.mjs')
const releaseLine = '1.0.0-RC1'

const components = [
  {
    id: 'echo-native-contracts',
    artifactId: 'echo-native-contracts',
    root: 'native',
    sourcePath: 'echo-native-contracts/build/libs'
  },
  {
    id: 'echoaddonapi',
    artifactId: 'echoaddonapi',
    root: 'modules',
    sourcePath: 'addons/echoaddonapi/build/libs'
  },
  {
    id: 'echoadaptercore',
    artifactId: 'echoadaptercore',
    root: 'modules',
    sourcePath: 'addons/echoadaptercore/build/libs'
  },
  {
    id: 'echo-native-testkit',
    artifactId: 'echo-native-testkit',
    root: 'native',
    sourcePath: 'echo-native-testkit/build/libs'
  },
  {
    id: 'sdk-gradle-plugin',
    artifactId: 'echo-sdk-gradle-plugin',
    root: 'sdk',
    sourcePath: 'gradle-plugin/echo-addon-gradle-plugin/build/libs'
  }
]

const classifiers = [
  { classifier: 'main', suffix: '.jar' },
  { classifier: 'sources', suffix: '-sources.jar' },
  { classifier: 'javadoc', suffix: '-javadoc.jar' }
]

function artifactName(component, classifier) {
  return `${component.artifactId}-${releaseLine}${classifier.suffix}`
}

function run(paths, args = []) {
  return spawnSync(process.execPath, [
    script,
    '--sdk-root',
    paths.sdk,
    '--native-platform-root',
    paths.native,
    '--modules-root',
    paths.modules,
    '--out',
    paths.out,
    ...args
  ], {
    encoding: 'utf8',
    windowsHide: true
  })
}

async function writeArtifacts(paths, options = {}) {
  const skip = new Set(options.skip ?? [])

  for (const component of components) {
    const root = paths[component.root]
    const dir = path.join(root, component.sourcePath)
    await fs.mkdir(dir, { recursive: true })
    for (const classifier of classifiers) {
      const name = artifactName(component, classifier)
      if (skip.has(name)) continue
      await fs.writeFile(path.join(dir, name), `fixture ${component.id} ${classifier.classifier}\n`, 'utf8')
    }
  }
}

async function withFixture(name, body) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), `echo-sdk-stage-${name}-`))
  const paths = {
    root,
    sdk: path.join(root, 'ECHO-SDK'),
    native: path.join(root, 'ECHO-Native-Platform'),
    modules: path.join(root, 'ECHO-Modules'),
    out: path.join(root, 'ECHO-SDK', 'dist', 'native-sdk-rc1')
  }
  try {
    await fs.mkdir(paths.sdk, { recursive: true })
    await body(paths)
  } finally {
    await fs.rm(root, { recursive: true, force: true })
  }
}

await withFixture('complete', async (paths) => {
  await writeArtifacts(paths)
  const result = run(paths, ['--clean', '--require-complete'])
  assert.equal(result.status, 0, result.stderr)
  const manifest = JSON.parse(result.stdout)
  assert.equal(manifest.schemaVersion, 'echo.native_sdk.rc1.workflow-release.v1')
  assert.equal(manifest.status, 'PASS')
  assert.equal(manifest.summary.componentCount, 5)
  assert.equal(manifest.summary.requiredArtifactCount, 15)
  assert.equal(manifest.summary.stagedArtifactCount, 15)
  assert.equal(manifest.artifacts.length, 15)
  assert.ok(manifest.artifacts.every((artifact) => /^[a-f0-9]{64}$/u.test(artifact.sha256)))

  const stagedNames = new Set((await fs.readdir(paths.out)).filter((name) => name.endsWith('.jar')))
  assert.equal(stagedNames.size, 15)
  const checksums = await fs.readFile(path.join(paths.out, 'checksums.sha256'), 'utf8')
  assert.equal(checksums.trim().split(/\r?\n/u).length, 15)
  const firstArtifact = manifest.artifacts[0]
  const bytes = await fs.readFile(path.join(paths.out, firstArtifact.file))
  assert.equal(firstArtifact.sha256, crypto.createHash('sha256').update(bytes).digest('hex'))
})

await withFixture('missing-javadoc', async (paths) => {
  const missing = 'echoadaptercore-1.0.0-RC1-javadoc.jar'
  await writeArtifacts(paths, { skip: [missing] })
  const result = run(paths, ['--clean', '--require-complete'])
  assert.notEqual(result.status, 0, 'missing javadoc must block complete staging')
  const manifest = JSON.parse(result.stdout)
  assert.equal(manifest.status, 'BLOCKED')
  assert.equal(manifest.summary.requiredArtifactCount, 15)
  assert.equal(manifest.summary.stagedArtifactCount, 14)
  assert.ok(manifest.blockers.includes(`echoadaptercore missing javadoc jar ${missing}`))
})

console.log('Native SDK RC1 staging fixtures passed.')
