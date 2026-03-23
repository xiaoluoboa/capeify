from wand.image import Image


def get_resolution_choice(cur_file):
    """列出所有分辨率并让用户选择，返回索引"""
    with Image(filename=cur_file) as cur:
        resolutions = sorted(
            cur.sequence, 
            key=lambda im: im.width * im.height
        )
        
        print("\n可用的鼠标分辨率:")
        for idx, img in enumerate(resolutions):
            print(f"  [{idx}] {img.width}x{img.height} ({img.width * img.height} 像素)")
        
        try:
            resolution_index = int(input("\n请选择分辨率索引 (0-{}): ".format(len(resolutions) - 1)))
            if 0 <= resolution_index < len(resolutions):
                selected = resolutions[resolution_index]
                print(f"已选择: {selected.width}x{selected.height}\n")
                return resolution_index
        except ValueError:
            pass
        
        print("输入无效，使用最小分辨率 (索引 0)\n")
        return 0


def convert_cur2png(cur_file, resolution_index=None):
    """根据指定索引转换分辨率"""
    with Image(filename=cur_file) as cur:
        resolutions = sorted(
            cur.sequence, 
            key=lambda im: im.width * im.height
        )
        
        if resolution_index is None:
            resolution_index = 0
        
        selected = resolutions[resolution_index]

        with Image(image=selected) as img:
            img.format = "png"
            png_data = img.make_blob()

    return png_data