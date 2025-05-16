"""
ファイル選択ダイアログを表示するためのモジュール
"""

import tkinter as tk
from tkinter import filedialog

from mov2gif.app_logger import AppLogger


class FileSelector:
    """
    tkinterを使用してファイル選択ダイアログを表示するクラス
    """

    def __init__(self, logger: AppLogger):
        """
        FileSelectorのコンストラクタ
        """
        self.logger = logger

    def show_dialog(self) -> str:
        """
        ファイル選択ダイアログを表示し、選択されたファイルのパスを返す

        Returns:
            str: 選択されたファイルのパス（キャンセル時は空文字列）
        """
        try:
            # tkinterのルートウィンドウを作成し非表示に
            root = tk.Tk()
            root.withdraw()

            # ファイル選択ダイアログを表示
            file_path = filedialog.askopenfilename(
                title="変換するMOVファイルを選択",
                filetypes=[("MOV動画ファイル", "*.mov"), ("すべてのファイル", "*.*")],
            )

            # tkinterのルートウィンドウを破棄
            root.destroy()

            if file_path:
                self.logger.info(f"ファイルが選択されました: {file_path}")
            else:
                self.logger.info("ファイル選択がキャンセルされました")

            return file_path

        except Exception as e:
            self.logger.error(
                f"ファイル選択ダイアログ表示中にエラーが発生しました: {str(e)}"
            )
            return ""
