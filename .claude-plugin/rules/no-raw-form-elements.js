/**
 * no-raw-form-elements
 *
 * Flags raw HTML form elements in .vue files when @nuxt/ui is installed.
 * Raw elements: input, button, form, select, textarea
 *
 * Does NOT flag elements inside <client-only> or <template #fallback>.
 */

const FORBIDDEN_TAGS = ['input', 'button', 'form', 'select', 'textarea'];
const NUXT_UI_IMPORT = '@nuxt/ui';

// Cache the check so we only read package.json once per ESLint run
let _hasNuxtUi = null;

function hasNuxtUiInPackageJson() {
  if (_hasNuxtUi !== null) return _hasNuxtUi;
  try {
    const cwd = typeof process !== 'undefined' ? process.cwd() : '.';
    const packageJsonPath = require('path').join(cwd, 'package.json');
    const pkg = JSON.parse(require('fs').readFileSync(packageJsonPath, 'utf8'));
    _hasNuxtUi = Boolean(
      (pkg.dependencies && pkg.dependencies[NUXT_UI_IMPORT]) ||
      (pkg.devDependencies && pkg.devDependencies[NUXT_UI_IMPORT])
    );
  } catch {
    _hasNuxtUi = false;
  }
  return _hasNuxtUi;
}

module.exports = {
  meta: {
    type: 'problem',
    docs: {
      description:
        'Disallow raw HTML form elements when @nuxt/ui is installed',
      recommended: true,
    },
    fixable: null,
    schema: [],
  },
  create(context) {
    // Check once at rule load time
    if (!hasNuxtUiInPackageJson()) {
      return {};
    }

    return {
      // Match any opening tag that is a forbidden form element
      'VElement > VTag > VIdentifier'(node) {
        const parent = node.parent;
        if (!parent || parent.name !== 'template') return;

        const tagName = node.value;
        if (!FORBIDDEN_TAGS.includes(tagName)) return;

        // Check if inside <client-only> or <template #fallback>
        let ancestor = node.parent;
        while (ancestor) {
          if (ancestor.name === 'client-only') return;
          if (
            ancestor.name === 'template' &&
            ancestor.startTag &&
            ancestor.startTag.attributes &&
            ancestor.startTag.attributes.some(
              (a) => a.key && a.key.name === 'slot' && a.key.argument && a.key.argument.name === 'fallback'
            )
          ) {
            return;
          }
          ancestor = ancestor.parent;
        }

        const ucTag = tagName.charAt(0).toUpperCase() + tagName.slice(1);
        context.report({
          node,
          message: `Raw <${tagName}> found. Use <U${ucTag}> from @nuxt/ui instead. See: https://ui.nuxt.dev/components/${tagName}`,
        });
      },
    };
  },
};