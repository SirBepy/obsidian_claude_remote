from PIL import Image, ImageDraw

SIZE = 256
BG = (15, 10, 31, 255)
GEM_MAIN = (124, 58, 237, 255)
GEM_LIGHT = (167, 139, 250, 255)
GEM_DARK = (91, 33, 182, 255)
DOT_OUTER = (249, 115, 22, 255)
DOT_INNER = (254, 215, 170, 255)


def draw(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = size * 48 // 256
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)

    s = size / 256
    top = (128 * s, 36 * s)
    right = (208 * s, 128 * s)
    bottom = (128 * s, 220 * s)
    left = (48 * s, 128 * s)
    center = (128 * s, 128 * s)

    d.polygon([top, right, bottom, left], fill=GEM_MAIN)
    d.polygon([top, right, center], fill=GEM_LIGHT)
    d.polygon([top, left, center], fill=GEM_DARK)

    cx, cy = 196 * s, 60 * s
    ro = 18 * s
    ri = 8 * s
    d.ellipse([cx - ro, cy - ro, cx + ro, cy + ro], fill=DOT_OUTER)
    d.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], fill=DOT_INNER)
    return img


def main() -> None:
    img256 = draw(256)
    img256.save("assets/images/favicon.png", "PNG")
    sizes = [16, 24, 32, 48, 64, 128, 256]
    imgs = [draw(s) for s in sizes]
    imgs[0].save(
        "icon.ico",
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=imgs[1:],
    )
    print("wrote assets/images/favicon.png and icon.ico")


if __name__ == "__main__":
    main()
