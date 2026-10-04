"""Styled QR code as inline SVG: round data modules, standard square finder patterns — for the deck and the site.
Dark modules on a light plate (plate=…) is the safe form: many scanners do not read light-on-dark codes.
The build checks that the code decodes (review/pp: crop from the page screenshot → OpenCV), see README."""
import segno

def qr_svg(url, size=120, ink="#141414", cls="qr", plate=None, quiet=None):
    q = segno.make(url, error="m", boost_error=False)
    m = q.matrix; n = len(m)
    if quiet is None: quiet = 4 if plate else 1          # the standard quiet zone is 4 modules; on a matching page background 1 is enough
    total = n + quiet * 2
    cell = size / total
    # commas in viewBox: typo() turns «0 112» into a thin-space number group and the attribute stops parsing
    out = [f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0,0,{size:.2f},{size:.2f}" width="{size}" height="{size}" role="img" aria-label="QR-код: {url}">']
    if plate: out.append(f'<rect x="0" y="0" width="{size:.2f}" height="{size:.2f}" rx="{cell * 2.2:.2f}" fill="{plate}" />')
    finders = [(0, 0), (0, n - 7), (n - 7, 0)]
    def in_finder(r, c):
        return any(fr <= r < fr + 7 and fc <= c < fc + 7 for fr, fc in finders)
    for fr, fc in finders:
        x = (fc + quiet) * cell; y = (fr + quiet) * cell
        # finder patterns stay standard squares: rounding them drops decoding from 14/14 to 2–9/14 test readings (scale × blur, OpenCV)
        out.append(f'<rect x="{x + cell / 2:.2f}" y="{y + cell / 2:.2f}" width="{6 * cell:.2f}" height="{6 * cell:.2f}" fill="none" stroke="{ink}" stroke-width="{cell:.2f}" />')
        out.append(f'<rect x="{x + 2 * cell:.2f}" y="{y + 2 * cell:.2f}" width="{3 * cell:.2f}" height="{3 * cell:.2f}" fill="{ink}" />')
    for r in range(n):                                   # data modules — touching dots (r = 0.5): the styled part that does not cost readability
        for c in range(n):
            if m[r][c] and not in_finder(r, c):
                out.append(f'<circle cx="{(c + quiet + .5) * cell:.2f}" cy="{(r + quiet + .5) * cell:.2f}" r="{cell * 0.5:.2f}" fill="{ink}" />')
    out.append("</svg>")
    return "".join(out)

if __name__ == "__main__":
    print(qr_svg("https://t.me/OBIIMY_sales")[:200])
