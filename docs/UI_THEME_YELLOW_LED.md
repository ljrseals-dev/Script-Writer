# Yellow LED Writer's Room Theme

The MUSE-GM Writer's Room uses a restrained yellow-LED visual language: warm amber/yellow illumination on a near-black work surface. The treatment is intended to feel like a focused studio console rather than a decorative neon page.

## Visual tokens

| Token | Value | Use |
|---|---|---|
| Background | `#090a08` | Main canvas |
| Panel | `#11130f` | Header and primary work surfaces |
| Raised panel | `#171a13` | Message cards |
| Primary text | `#f5f3df` | Main copy |
| Muted text | `#b8b99e` | Supporting copy |
| LED yellow | `#ffe94a` | Active indicator, primary actions, focus |
| LED highlight | `#fff7a8` | Headings and highlighted links |
| LED dim | `#a99a22` | Borders and secondary emphasis |
| Success | `#a8d58b` | User approval / positive status accents |
| Warning | `#d49a56` | System notices |

## Interaction and accessibility

- The LED indicator is decorative; it does not claim that a service, model, or approval is active.
- Focus-visible outlines use the bright yellow token.
- Text and controls remain readable against the dark surfaces; color is not the only way message roles are distinguished.
- Layout collapses to a single-column composer on narrow screens.
- Reduced-motion preferences disable transitions.
- The existing session, ranking, approval, reset, and API behavior is unchanged by the theme.

## Scope

This theme is implemented in `muse_gm/static/index.html`. It is a presentation-layer change only. It does not change ranking calculations, evidence status, approval authorization, model behavior, or server security boundaries.
