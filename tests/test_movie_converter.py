"""
movie_converter モジュールのテスト
"""

import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from mov2gif.movie_converter import MovieConverter
from mov2gif.app_logger import AppLogger


class TestMovieConverter:
    @pytest.fixture
    def setup_converter():
        """テスト実行前の準備"""
        mock_logger = MagicMock(spec=AppLogger)
        converter = MovieConverter(mock_logger)
        temp_dir = tempfile.TemporaryDirectory()
        test_mov_path = str(Path(temp_dir.name) / "test.mov")
        test_gif_path = str(Path(temp_dir.name) / "test.gif")

        # テスト用に空のmovファイルを作成
        with open(test_mov_path, "w") as f:
            f.write("dummy content")

        yield converter, mock_logger, temp_dir, test_mov_path, test_gif_path

        # テスト実行後のクリーンアップ
        temp_dir.cleanup()

    @patch("moviepy.VideoFileClip")
    def test_mov_to_gif_success(mock_video_file_clip, setup_converter):
        """正常系: 変換が成功する場合"""
        converter, mock_logger, _, test_mov_path, test_gif_path = setup_converter

        # モックの設定
        mock_clip = MagicMock()
        mock_video_file_clip.return_value = mock_clip

        # テスト対象メソッド呼び出し
        result = converter.mov_to_gif(test_mov_path, test_gif_path)

        # 検証
        assert result is True
        mock_video_file_clip.assert_called_once_with(test_mov_path)
        mock_clip.write_gif.assert_called_once()
        mock_clip.close.assert_called_once()

        # ロガーの確認
        mock_logger.info.assert_any_call(
            f"変換開始: {test_mov_path} -> {test_gif_path}"
        )
        mock_logger.info.assert_any_call(f"変換完了: {test_gif_path}")

    @patch("moviepy.VideoFileClip")
    def test_mov_to_gif_default_output_path(mock_video_file_clip, setup_converter):
        """正常系: 出力パスが指定されない場合、デフォルト値が使用される"""
        converter, _, _, test_mov_path, _ = setup_converter

        # モックの設定
        mock_clip = MagicMock()
        mock_video_file_clip.return_value = mock_clip

        # テスト対象メソッド呼び出し（出力パス省略）
        result = converter.mov_to_gif(test_mov_path)

        # 検証 - 拡張子がgifに変更されたパスが使用されること
        expected_output = str(Path(test_mov_path).with_suffix(".gif"))
        assert result is True
        mock_clip.write_gif.assert_called_once()

        # write_gifの引数を確認
        args, kwargs = mock_clip.write_gif.call_args
        assert args[0] == expected_output

    @patch("moviepy.VideoFileClip", side_effect=Exception("Test error"))
    def test_mov_to_gif_failure(mock_video_file_clip, setup_converter):
        """異常系: 変換中にエラーが発生する場合"""
        converter, mock_logger, _, test_mov_path, test_gif_path = setup_converter

        # テスト対象メソッド呼び出し
        result = converter.mov_to_gif(test_mov_path, test_gif_path)

        # 検証 - 失敗時はFalseが返されること
        assert result is False
        mock_video_file_clip.assert_called_once_with(test_mov_path)

        # エラーログが出力されていることを確認
        mock_logger.error.assert_called_once()

    @patch("mov2gif.movie_converter.MovieConverter.mov_to_gif")
    def test_batch_convert_all_success(mock_convert, setup_converter):
        """正常系: すべてのファイルが正常に変換される場合"""
        converter, mock_logger, temp_dir, test_mov_path, _ = setup_converter

        # モックの設定
        mock_convert.return_value = True

        # テスト用のファイルパスリスト
        file_paths = [
            test_mov_path,
            str(Path(temp_dir.name) / "test2.mov"),
            str(Path(temp_dir.name) / "test3.mov"),
        ]

        # テスト対象メソッド呼び出し
        results = converter.batch_convert(file_paths)

        # 検証
        assert len(results) == len(file_paths)
        assert mock_convert.call_count == len(file_paths)
        for path in file_paths:
            assert results[path] is True

        # ログ出力の確認
        mock_logger.info.assert_any_call(
            f"{len(file_paths)}個のファイルの変換を開始します"
        )

    @patch("mov2gif.movie_converter.MovieConverter.mov_to_gif")
    def test_batch_convert_partial_failure(mock_convert, setup_converter):
        """異常系: 一部のファイルの変換が失敗する場合"""
        converter, mock_logger, temp_dir, test_mov_path, _ = setup_converter

        # モックの設定 - 2番目のファイルだけ失敗する
        mock_convert.side_effect = [True, False, True]

        # テスト用のファイルパスリスト
        file_paths = [
            test_mov_path,
            str(Path(temp_dir.name) / "test2.mov"),
            str(Path(temp_dir.name) / "test3.mov"),
        ]

        # テスト対象メソッド呼び出し
        results = converter.batch_convert(file_paths)

        # 検証
        assert len(results) == len(file_paths)
        assert mock_convert.call_count == len(file_paths)
        assert results[file_paths[0]] is True
        assert results[file_paths[1]] is False
        assert results[file_paths[2]] is True

        # サマリーログの確認
        success_count = 2  # 1つ目と3つ目が成功
        mock_logger.info.assert_any_call(
            f"変換完了: {success_count}/{len(file_paths)} 成功"
        )

    def test_batch_convert_empty_list(setup_converter):
        """正常系: 空のリストが渡された場合"""
        converter, mock_logger, _, _, _ = setup_converter

        # テスト対象メソッド呼び出し
        results = converter.batch_convert([])

        # 検証 - 空の辞書が返されること
        assert results == {}

        # 警告ログが出力されていることを確認
        mock_logger.warning.assert_called_once_with(
            "変換対象ファイルが指定されていません"
        )
