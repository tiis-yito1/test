#!/usr/bin/env python3
import argparse
import json
import os
import pptx
import pptx.api
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE

# Monkey-patch to support .potx templates
_original_is_pptx_package = pptx.api._is_pptx_package
def _patched_is_pptx_package(prs_part):
    if prs_part.content_type == 'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml':
        return True
    return _original_is_pptx_package(prs_part)
pptx.api._is_pptx_package = _patched_is_pptx_package

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a PowerPoint presentation from a JSON file using a template.")
    parser.add_argument("--data", required=True, help="Path to the JSON file with presentation content.")
    parser.add_argument("--template", required=True, help="Path to the PowerPoint template file.")
    parser.add_argument("--output", required=True, help="Path to the output PowerPoint file.")
    # --- 画像挿入用の引数を追加 ---
    parser.add_argument("--image", help="Path to an image to insert into the slide.")
    return parser.parse_args()

def add_slide_with_content(prs, slide_data, layout, image_path=None):
    slide = prs.slides.add_slide(layout)

    # ... (既存のテキストクリア処理) ...
    for shape in slide.shapes:
        is_fixed_placeholder = False
        try:
            ph_type = shape.placeholder_format.type
            if ph_type in [PP_PLACEHOLDER.SLIDE_NUMBER, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.DATE]:
                is_fixed_placeholder = True
        except AttributeError:
            pass
        if not is_fixed_placeholder and shape.has_text_frame:
            shape.text_frame.clear()

    # ... (既存のタイトル・本文書き込み処理) ...
    if slide.shapes.title:
        slide.shapes.title.text = slide_data.get("title", "")
    
    body_shape = None
    for shape in slide.placeholders:
        if shape.placeholder_format.type == PP_PLACEHOLDER.BODY:
            body_shape = shape
            break
    
    if body_shape:
        tf = body_shape.text_frame
        body_text = slide_data.get("content", {}).get("body", "")
        # ... (既存の段落処理) ...
        lines = body_text.split('\\n')
        if lines:
            p = tf.paragraphs[0]; p.text = lines[0]
            if lines[0].strip().startswith('・'): p.level = 1
        for line in lines[1:]:
            p = tf.add_paragraph(); p.text = line
            if line.strip().startswith('・'): p.level = 1

    # --- 画像挿入処理を追加 ---
    if image_path:
        # 画像のサイズや位置はここで調整可能
        # とりあえず中央に配置する例
        left = Inches(1.5)
        top = Inches(2.5)
        height = Inches(4.0)
        slide.shapes.add_picture(image_path, left, top, height=height)

    return slide

def main():
    args = parse_args()

    try:
        with open(args.data, 'r', encoding='utf-8') as f:
            slides_content = json.load(f)
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    prs = Presentation(args.template)
    
    title_slide_layout = prs.slide_layouts[0]
    content_slide_layout = prs.slide_layouts[2]

    # --- Mermaidからの画像パスを考慮し、ループをシンプルに ---
    for i, slide_data in enumerate(slides_content):
        image_path = slide_data.get("image")
        layout = title_slide_layout if i == 0 else content_slide_layout
        
        # 本文がない場合は画像だけ挿入するスライドも考慮
        if slide_data.get("content", {}).get("body") or image_path:
             add_slide_with_content(prs, slide_data, layout, image_path=image_path)


    try:
        # ... (既存の二重保存処理) ...
        temp_path = args.output + ".tmp.pptx"
        prs.save(temp_path)
        final_prs = Presentation(temp_path)
        final_prs.save(args.output)
        os.remove(temp_path)
        print(f"Successfully created presentation at {args.output}")
    except Exception as e:
        print(f"Error saving presentation: {e}")

if __name__ == "__main__":
    main()
