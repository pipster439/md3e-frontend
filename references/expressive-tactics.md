# Expressive tactics

Source: <https://m3.material.io/blog/building-with-m3-expressive>

M3E is not just new tokens. Google distilled a set of design tactics for
directing attention, each one an axis along which a component, layout or
product can be made more expressive. They are the *why* behind the tokens.

## Why it works (the research)

The update rests on 46 studies with more than 18,000 participants. Findings:

- Expressive designs are preferred by people of all ages.
- They score consistently higher on playfulness, energy, creativity and
  friendliness.
- **Users spot key UI elements up to four times faster** in expressive screens.
- Users are more likely to switch to products that use Expressive components.

So expressiveness is a usability lever, not decoration. That is the framing to
use when someone asks whether the extra rounding and motion are worth it.

M3E is **not** a new version. It does not deprecate M3, and it is not "M4". It
is an evolution of M3: new features, updated components, and tactics.

## The seven tactics

1. **Use a variety of shapes.** Shape sets the tone at first glance. Combine
   shapes and corner radii to create tension or cohesion and to direct focus.
   Use the shape library and the new corner radii to mix round and square.
   *Caution:* a shape that is too small can make an essential action look
   unimportant. Breaking from the surrounding shape language draws attention.

2. **Apply rich and nuanced colours.** Mix primary, secondary and tertiary
   roles on key components to emphasise the screen's main takeaway. Build
   hierarchy with surface tones and use role contrast to prioritise actions.
   *Caution:* without contrast, elements blend together.

3. **Guide attention with typography.** Emphasized type styles on headlines and
   actions. Heavier weights, larger sizes, colour and spacing create
   editorial-style moments and reinforce hierarchy.
   *Caution:* emphasis everywhere is emphasis nowhere.

4. **Contain content for emphasis.** Group content into logical containers and
   give the most important content the most space and the brightest surface
   mapping. Use size, spacing, rhythm and similarity to make things distinct.
   *Caution:* ungrouped information blends together.

5. **Add fluid and natural motion.** Make interactions feel alive through shape
   morph and surface effects, driven by the motion springs or custom
   micro-animations. Motion should reveal state, progress or causality — never
   decorate.

6. **Leverage component flexibility.** Adapt the UI to context: shift
   components or controls depending on the environment, and use canonical
   layouts for foldables and large screens. Flexibility beats a fixed layout
   that happens to fit one device.

7. **Combine tactics to create hero moments.** Hero moments layer several
   tactics and break from predictable, uniformly applied design. They frame
   essential information editorially and act as a focusing mechanism.

## Hero moments

- Brief, delightful, surprising, unexpected.
- Use sparingly, in places where the extra emphasis clarifies the experience.
- Ask two questions before building one:

  1. *Is this interaction emotionally impactful?* Does the choice highlight an
     emotional reaction or reinforce familiarity?
  2. *Is this a key interaction in the product?* Can it be emphasised for
     clarity — a dominant primary button, key information made unmistakable?

Invest effort where it changes the product's feel, not on every screen.

## Applying this to a build

A practical order that avoids the usual failure mode (everything expressive, so
nothing is):

1. Get the base compliant first — roles, type scale, shape scale, springs. A
   screen that follows the system already reads as Material.
2. Pick a meaningful hero moment. Spend the tension, morphing and
   emphasis budget there.
3. Apply one or two secondary tactics elsewhere — usually a surface-tone
   hierarchy for grouping (tactic 4) and emphasized type on the primary action
   (tactic 3).
4. Re-run the auditor and review findings in context. Keep custom colours,
   radii and timing intentional and accessible.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Expressiveness at every level | Nothing stands out; the interface reads as noisy |
| Springs everywhere, including colour | Colour must not overshoot |
| Expressive shape on dense content | Corners clip data; readability drops |
| Tertiary accents on every element | The accent stops meaning "look here" |
| Emphasized type on all headings | Hierarchy collapses to a single tier |
| Motion with no trigger | Reads as lag, not liveliness |
| Hero moments on every screen | Becomes the baseline, so it stops being a moment |
