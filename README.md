# ColorHints
Inline color hints for Sublime Text

![](https://raw.githubusercontent.com/braver/ColorHints/master/Colors.gif)

Call up an inline color box displaying the color at the cursor(s). Live hints can be enabled always, never, or just in specific languages (via [scope selectors](https://www.sublimetext.com/docs/3/selectors.html)). The manually called hints will stick around until the file is edited.

ColorHints currently understands:

- hex(a)<sup>*</sup>
- rgb(a)
- hsl(a)
- hwb(a)
- css color names (e.g. "aliceblue" or "rebeccapurple")
- Pantone color codes (e.g. "16-1546 TCX" or "Yellow 012 C")
- RAL classic color codes (e.g. "RAL 6034")

<sup>*</sup>) Set the "argb_hex" preference to `true` for (a)hex, ie. argb in hex values.

## Notes

The alpha (opacity) value is not represented in the hint. In these small samples it's impossible to properly judge the opacity anyway, and it's usually more interesting to know the base color. 

Thanks to [@facelessuser](https://github.com/facelessuser) for the [utils and libraries](https://github.com/facelessuser/ColorHelper) that make this possible. The Pantone reference files were dowloaded from [Pantone.com](https://www.pantone.com).

## Related color utilities

This plugin just does what it says on the box: display color hints. Other packages do other nifty things with colors:

- Convert colors between RGB, Hex, HSL, etc: [Color Convert](https://packagecontrol.io/packages/Color%20Convert)
- Integrate with OS native [Color picker](https://packagecontrol.io/packages/ColorPicker)

## Buy me a coffee 

☕️👌🏻

Please feel free to make a little [donation via PayPal](https://paypal.me/koenlageveen) towards the coffee that keeps this labour of love running. It's much appreciated!
