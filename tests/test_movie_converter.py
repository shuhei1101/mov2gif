"""
movie_converter モジュールのテスト
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mov2gif.movie_converter import MovieConverter


class TestMovieConverter(unittest.TestCase):
    """MovieConverterクラスのテスト"""

    def setUp(self):
        """テスト実行前の準備"""
        self.converter = MovieConverter()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_mov_path = str(Path(self.temp_dir.name) / "test.mov")
        self.test_gif_path = str(Path(self.temp_dir.name) / "test.gif")

        # テスト用に空のmovファイルを作成
        with open(self.test_mov_path, "w") as f:
            f.write("dummy content")

    def tearDown(self):
        """テスト実行後のクリーンアップ"""
        self.temp_dir.cleanup()

    @patch("moviepy.editor.VideoFileClip")
    def test_convert_to_gif_success(self, mock_video_file_clip):
        """正常系: 変換が成功する場合"""
        # モックの設定
        mock_clip = MagicMock()
        mock_video_file_clip.return_value = mock_clip

        # テスト対象メソッド呼び出し
        result = self.converter.convert_to_gif(self.test_mov_path, self.test_gif_path)

        # 検証
        self.assertTrue(result)
        mock_video_file_clip.assert_called_once_with(self.test_mov_path)
        mock_clip.write_gif.assert_called_once()
        mock_clip.close.assert_called_once()

    @patch("moviepy.editor.VideoFileClip")
    def test_convert_to_gif_default_output_path(self, mock_video_file_clip):
        """正常系: 出力パスが指定されない場合、デフォルト値が使用される"""
        # モックの設定
        mock_clip = MagicMock()
        mock_video_file_clip.return_value = mock_clip

        # テスト対象メソッド呼び出し（出力パス省略）
        result = self.converter.convert_to_gif(self.test_mov_path)

        # 検証 - 拡張子がgifに変更されたパスが使用されること
        expected_output = str(Path(self.test_mov_path).with_suffix(".gif"))
        self.assertTrue(result)
        mock_clip.write_gif.assert_called_once()
        # write_gifの引数を確認
        args, _ = mock_clip.write_gif.call_args
        self.assertEqual(args[0], expected_output)

    @patch("moviepy.editor.VideoFileClip", side_effect=Exception("Test error"))
    def test_convert_to_gif_failure(self, mock_video_file_clip):
        """異常系: 変換中にエラーが発生する場合"""
        # テスト対象メソッド呼び出し
        result = self.converter.convert_to_gif(self.test_mov_path, self.test_gif_path)

        # 検証 - 失敗時はFalseが返されること
        self.assertFalse(result)
        mock_video_file_clip.assert_called_once_with(self.test_mov_path)

    @patch("mov2gif.movie_converter.MovieConverter.convert_to_gif")
    def test_batch_convert_all_success(self, mock_convert):
        """正常系: すべてのファイルが正常に変換される場合"""
        # モックの設定
        mock_convert.return_value = True

        # テスト用のファイルパスリスト
        file_paths = [
            self.test_mov_path,
            str(Path(self.temp_dir.name) / "test2.mov"),
            str(Path(self.temp_dir.name) / "test3.mov"),
        ]

        # テスト対象メソッド呼び出し
        results = self.converter.batch_convert(file_paths)

        # 検証
        self.assertEqual(len(results), len(file_paths))
        self.assertEqual(mock_convert.call_count, len(file_paths))
        for path in file_paths:
            self.assertTrue(results[path])

    @patch("mov2gif.movie_converter.MovieConverter.convert_to_gif")
    def test_batch_convert_partial_failure(self, mock_convert):
        """異常系: 一部のファイルの変換が失敗する場合"""
        # モックの設定 - 2番目のファイルだけ失敗する
        mock_convert.side_effect = [True, False, True]

        # テスト用のファイルパスリスト
        file_paths = [
            self.test_mov_path,
            str(Path(self.temp_dir.name) / "test2.mov"),
            str(Path(self.temp_dir.name) / "test3.mov"),
        ]

        # テスト対象メソッド呼び出し
        results = self.converter.batch_convert(file_paths)

        # 検証
        self.assertEqual(len(results), len(file_paths))
        self.assertEqual(mock_convert.call_count, len(file_paths))
        self.assertTrue(results[file_paths[0]])
        self.assertFalse(results[file_paths[1]])
        self.assertTrue(results[file_paths[2]])

    def test_batch_convert_empty_list(self):
        """正常系: 空のリストが渡された場合"""
        # テスト対象メソッド呼び出し
        results = self.converter.batch_convert([])

        # 検証 - 空の辞書が返されること
        self.assertEqual(results, {})


if __name__ == "__main__":
    unittest.main()
