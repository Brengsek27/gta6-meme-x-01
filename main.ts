import { copyFileSync, mkdirSync } from 'node:fs';
import { join, resolve, sep } from 'node:path';
import { pathToFileURL } from 'node:url';

const botDirectory = process.env.MAKEFUN_BOT_DIR;
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = botDirectory === undefined
  ? new URL('./POST.json', import.meta.url)
  : new URL('./POST.json', pathToFileURL(resolve(botDirectory) + sep));

mkdirSync(outputDirectory, { recursive: true });
copyFileSync(source, join(outputDirectory, 'POST.json'));
