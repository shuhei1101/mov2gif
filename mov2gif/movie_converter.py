"""
MOV形式の動画をGIF形式に変換するためのモジュール
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional
import moviepy.editor

# ロガーの設定
logger = logging.getLogger(__name__)


class MovieConverter:
    """
    MOV動画ファイルをGIFに変換するクラス
    """

    def __init__(self):
        """
        MovieConverterのコンストラクタ
        """
        pass

    def convert_to_gif(
        self, input_path: str, output_path: Optional[str] = None
    ) -> bool:
        """
        単一のMOVファイルをGIFに変換する

        Args:
            input_path (str): 入力MOVファイルのパス
            output_path (str, optional): 出力GIFファイルのパス。未指定の場合は入力ファイルと同じ場所に同名で保存

        Returns:
            bool: 変換成功時はTrue、失敗時はFalse
        """
        try:
            # 出力パスが指定されていない場合はデフォルトパスを使用
            if output_path is None:
                output_path = str(Path(input_path).with_suffix(".gif"))

            logger.info(f"変換開始: {input_path} -> {output_path}")

            # MoviePyを使用して変換
            clip = VideoFileClip(input_path)

            # GIFに変換（低品質オプションでファイルサイズを削減）
            clip.write_gif(
                output_path,
                fps=15,  # フレームレートを15fpsに設定
                opt="OptimizeTransparency",  # 透明度最適化
            )

            # クリップを閉じる（リソース解放）
            clip.close()

            logger.info(f"変換完了: {output_path}")
            return True

        except Exception as e:
            logger.error(f"変換中にエラーが発生しました: {str(e)}")
            return False

    def batch_convert(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        複数のMOVファイルを一括でGIFに変換する

        Args:
            file_paths (List[str]): 変換対象のMOVファイルパスのリスト

        Returns:
            Dict[str, bool]: 変換結果の辞書 {ファイルパス: 成功/失敗}
        """
        results = {}

        if not file_paths:
            logger.warning("変換対象ファイルが指定されていません")
            return results

        logger.info(f"{len(file_paths)}個のファイルの変換を開始します")

        # 各ファイルを順番に変換
        for path in file_paths:
            result = self.convert_to_gif(path)
            results[path] = result

        # 結果サマリーを作成
        success_count = sum(1 for result in results.values() if result)
        logger.info(f"変換完了: {success_count}/{len(file_paths)} 成功")

        return results
