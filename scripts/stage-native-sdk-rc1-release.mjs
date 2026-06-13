#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'

const RELEASE_LINE = '1.0.0-RC1'
const DEFAULT_OUT = 'dist/native-sdk-rc1'

const components = [
  {
    id: 'echo-native-contracts',
    artifactId: 'echo-native-contracts',
    repoArg: 'nativePlatformRoot',
    sourcePath: 'echo-native-contracts/build/libs'
  },
  {
    id: 'echoaddonapi',
    artifactId: 'echoaddonapi',
    repoArg: 'modulesRoot',
    sourcePath: 'addons/echoaddonapi/build/libs'
  },
  {
    id: 'echoadaptercore',
    artifactId: 'echoadaptercore',
    repoArg: 'modulesRoot',
    sourcePath: 'addons/echoadaptercore/build/libs'
  },
  {
    id: 'echo-native-testkit',
    artifactId: 'echo-native-testkit',
    repoArg: 'nativePlatformRoot',
    sourcePath: 'echo-native-testkit/build/libs'
  },
  {
    id: 'sdk-gradle-plugin',
    artifactId: 'echo-sdk-gradle-plugin',
    repoArg: 'sdkRoot',
    sourcePath: 'gradle-plugin/echo-addon-gradle-plugin/build/libs'
  }
]

const classifiers = [
  { classifier: 'main', suffix: '.jar' },
  { classifier: 'sources', suffix: '-sources.jar' },
  { classifier: 'javadoc', suffix: '-javadoc.jar' }
]

function parseArgs(argv) {
  const args = {
    sdkRoot: process.cwd(),
    nativePlatformRoot: null,
    modulesRoot: null,
    out: DEFAULT_OUT,
    clean: false,
    requireComplete: false,
    help: false
  }

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index]
    if (arg === '--sdk-root') args.sdkRoot = path.resolve(argv[++index])
    else if (arg === '--native-platform-root') args.nativePlatformRoot = path.resolve(argv[++index])
    else if (arg === '--modules-root') args.modulesRoot = path.resolve(argv[++index])
    else if (arg === '--out') args.out = argv[++index]
    else if (arg === '--clean') args.clean = true
    else if (arg === '--require-complete') args.requireComplete = true
    else if (arg === '--help') args.help = true
    else throw new Error(`Unknown argument: ${arg}`)
  }

  args.sdkRoot = path.resolve(args.sdkRoot)
  args.nativePlatformRoot = args.nativePlatformRoot ?? path.resolve(args.sdkRoot, '..', 'ECHO-Native-Platform')
  args.modulesRoot = args.modulesRoot ?? path.resolve(args.sdkRoot, '..', 'ECHO-Modules')
  args.out = path.isAbsolute(args.out) ? args.out : path.join(args.sdkRoot, args.out)
  return args
}

function usage() {
  return `Usage: node scripts/stage-native-sdk-rc1-release.mjs [options]

Stages the 15 public Native SDK RC1 jars from their source build outputs.

Options:
  --sdk-root <dir>              ECHO-SDK root. Default: current directory.
  --native-platform-root <dir>  ECHO-Native-Platform root. Default: sibling of SDK.
  --modules-root <dir>          ECHO-Modules root. Default: sibling of SDK.
  --out <dir>                   Staging output directory. Default: ${DEFAULT_OUT}.
  --clean                       Delete the output directory before staging.
  --require-complete            Exit non-zero unless all 15 artifacts are present.
  --help                        Print this help text.
`
}

function rel(root, filePath) {
  return path.relative(root, filePath).replace(/\\/g, '/')
}

function expectedFiles(component) {
  return classifiers.map((classifier) => ({
    classifier: classifier.classifier,
    fileName: `${component.artifactId}-${RELEASE_LINE}${classifier.suffix}`
  }))
}

async function readFileEvidence(filePath) {
  try {
    const stat = await fs.stat(filePath)
    if (!stat.isFile()) return { exists: false, reason: 'not-file' }
    const bytes = await fs.readFile(filePath)
    return {
      exists: true,
      bytes,
      size: stat.size,
      sha256: crypto.createHash('sha256').update(bytes).digest('hex')
    }
  } catch (error) {
    if (error?.code === 'ENOENT') return { exists: false, reason: 'missing' }
    throw error
  }
}

async function stage(args) {
  if (args.clean) await fs.rm(args.out, { recursive: true, force: true })
  await fs.mkdir(args.out, { recursive: true })

  const blockers = []
  const stagedArtifacts = []
  const componentReports = []

  for (const component of components) {
    const repoRoot = args[component.repoArg]
    const sourceDir = path.join(repoRoot, component.sourcePath)
    const fileReports = []

    for (const expected of expectedFiles(component)) {
      const source = path.join(sourceDir, expected.fileName)
      const target = path.join(args.out, expected.fileName)
      const evidence = await readFileEvidence(source)
      const fileBlockers = []

      if (!evidence.exists) {
        fileBlockers.push(`${component.id} missing ${expected.classifier} jar ${expected.fileName}`)
      } else {
        await fs.copyFile(source, target)
        stagedArtifacts.push({
          component: component.id,
          classifier: expected.classifier,
          file: expected.fileName,
          sourcePath: rel(repoRoot, source),
          outputPath: rel(args.sdkRoot, target),
          size: evidence.size,
          sha256: evidence.sha256
        })
      }

      blockers.push(...fileBlockers)
      fileReports.push({
        classifier: expected.classifier,
        file: expected.fileName,
        sourcePath: rel(repoRoot, source),
        outputPath: evidence.exists ? rel(args.sdkRoot, target) : null,
        exists: evidence.exists,
        size: evidence.size,
        sha256: evidence.sha256,
        blockers: fileBlockers
      })
    }

    componentReports.push({
      id: component.id,
      artifactId: component.artifactId,
      sourceRoot: repoRoot,
      sourcePath: component.sourcePath,
      status: fileReports.every((file) => file.exists) ? 'PASS' : 'BLOCKED',
      files: fileReports
    })
  }

  const checksums = stagedArtifacts
    .slice()
    .sort((a, b) => a.file.localeCompare(b.file))
    .map((artifact) => `${artifact.sha256}  ${artifact.file}`)
    .join('\n')

  await fs.writeFile(path.join(args.out, 'checksums.sha256'), `${checksums}${checksums ? '\n' : ''}`, 'utf8')

  const manifest = {
    schemaVersion: 'echo.native_sdk.rc1.workflow-release.v1',
    status: blockers.length ? 'BLOCKED' : 'PASS',
    generatedAt: new Date().toISOString(),
    releaseLine: RELEASE_LINE,
    sdkRoot: args.sdkRoot,
    nativePlatformRoot: args.nativePlatformRoot,
    modulesRoot: args.modulesRoot,
    outputRoot: args.out,
    summary: {
      componentCount: components.length,
      requiredArtifactCount: components.length * classifiers.length,
      stagedArtifactCount: stagedArtifacts.length,
      totalBytes: stagedArtifacts.reduce((sum, artifact) => sum + artifact.size, 0)
    },
    components: componentReports,
    artifacts: stagedArtifacts,
    blockers,
    notes: [
      'This manifest is produced from source build outputs before GitHub Actions provenance attestation.',
      'A stable Release Index entry still requires attestation verification against these exact artifact digests.'
    ]
  }

  await fs.writeFile(path.join(args.out, 'native-sdk-rc1-manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`, 'utf8')
  return manifest
}

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (args.help) {
    process.stdout.write(usage())
    return
  }
  const manifest = await stage(args)
  console.log(JSON.stringify(manifest, null, 2))
  if (args.requireComplete && manifest.status !== 'PASS') process.exitCode = 1
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error))
  process.exitCode = 1
})
