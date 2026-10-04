#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 合并脚本 — 将施工记录PDF + 天气报告PDF + 潮汐预报PDF合并为完整版
=========================================================================
用途：独立合并工具，适用于手动生成PDF后的合并场景
依赖：pip install pypdf

使用方法：
    python merge_pdf.py --date 2026-08-02
"""

import os
import sys
import argparse
from pypdf import PdfWriter, PdfReader

BASE_DIR = r"<PROJECTS_ROOT>\[项目名称]\每日施工记录"


def merge(date_str):
    """合并施工记录 + 天气 + 潮汐为一个PDF"""
    construction_pdf = os.path.join(BASE_DIR, f"{date_str}每日施工记录表.pdf")
    weather_pdf = os.path.join(BASE_DIR, "附件", "天气报告", f"天气报告_{date_str}.pdf")
    tide_pdf = os.path.join(BASE_DIR, "附件", "潮汐预报", f"潮汐预报_{date_str}.pdf")
    output_pdf = os.path.join(BASE_DIR, f"{date_str}每日施工记录表_完整版.pdf")

    # 检查文件存在
    files = [
        ("施工记录PDF", construction_pdf),
        ("天气报告PDF", weather_pdf),
        ("潮汐预报PDF", tide_pdf),
    ]

    writer = PdfWriter()
    for label, path in files:
        if os.path.exists(path):
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
            print(f"✅ 已添加: {label} ({len(reader.pages)} 页)")
        else:
            print(f"⚠️  跳过不存在的文件: {label} ({path})")

    with open(output_pdf, 'wb') as f:
        writer.write(f)

    print(f"\n📄 合并完成: {output_pdf}")

    # 可选：替换原始施工记录PDF
    if os.path.exists(construction_pdf):
        os.remove(construction_pdf)
        os.rename(output_pdf, construction_pdf)
        print(f"🔄 已替换: {construction_pdf}")

    return construction_pdf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF合并工具")
    parser.add_argument("--date", required=True, help="日期 YYYY-MM-DD")
    args = parser.parse_args()

    merge(args.date)
