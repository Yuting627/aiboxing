import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { fileURLToPath } from 'url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(dir, '../..');

export default defineConfig({
  plugins: [react()],
  assetsInclude: ['**/*.glb'],
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
  build: {
    emptyOutDir: false,
    outDir: path.resolve(root, 'source/js'),
    lib: {
      entry: path.resolve(dir, 'main.jsx'),
      name: 'AboutLanyard',
      fileName: () => 'lanyard-bundle.js',
      formats: ['iife'],
    },
    rollupOptions: {
      output: {
        assetFileNames: 'lanyard-[name][extname]',
      },
    },
  },
});
