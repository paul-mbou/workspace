# Interface

La direction visuelle est un travail de produit, pas un thème collé à la fin. Les skills ci-dessous sont installés et se combinent. Quand un dépôt a déjà un design system, ce système gagne : palette, typographie et but du produit ne sont pas remplacés.

## Qui fait quoi

| Skill | Rôle |
| --- | --- |
| `ui-design-director` | orchestre les autres skills design |
| `frontend-design` | parti pris visuel : palette, type, layout, mouvement |
| `anti-ui-slop` | bloque l'UI générique d'agent |
| `ui-design-brain` | anatomie de composants (listes, sheets, formulaires, chat) |
| `ui-design` et `ui-radar` | références réelles UIZZE (web et iOS) |
| `ui-ux-pro-max` | UX, accessibilité, structure, notes Flutter |
| `typeui-fundamentals` | hiérarchie, typographie, WCAG |
| `true-ui-redesign` | change la disposition et la sensation, en gardant les couleurs du système local |

`ui-design-director` vit dans `~/.cursor/skills/ui-design-director` et sur `https://github.com/Endeavor068/ui-design-director`. Toute édition de ce skill est commitée et poussée.

Règle `web-design-quality` : ne pas livrer une interface qui pourrait être n'importe quel template. La page doit être spécifique au produit.

## Formulaires longs

Sur les apps qui suivent le kit Bricks / gold_stock : un formulaire long s'ouvre en sheet (`Modal variant="sheet"`), avec une navigation basse sur mobile. Les jetons de Bricks sont `slate`, `clay` et `br-*` (lavande, charcoal, lime). Le couple navy / or de gold_stock ne se réutilise pas dans Bricks.

Lumière par défaut, sombre via `.dark`, et `prefers-reduced-motion` respecté.

## Textes

- Produit destiné au Cameroun : interface en français, code en anglais.
- Pas de chaînes en dur hors des fichiers i18n ou data, quand le projet a déjà cette règle.
- Montants en FCFA, format local.

## Vérifier

1. Parcourir le flux modifié de bout en bout.
2. Ouvrir les autres routes qui lisent le même état.
3. Regarder vide, erreur, et variante de rôle ou de feature flag.
4. Si la mise en page a changé, regarder un viewport bureau et un viewport téléphone.
5. Largeurs de contrôle des règles web : 320, 768, 1024, 1440.

Outils : navigateur Cursor, Figma MCP pour un fichier source, Stitch pour une exploration d'écran, Maestro ou mobile-mcp pour une app.

## Accessibilité

`typeui-fundamentals` et `react-native-accessibility` traitent l'accessibilité comme un critère de livraison : contraste, cibles de toucher, labels, ordre de focus. Un composant joli et inutilisable au clavier ou au lecteur d'écran n'est pas fini.
