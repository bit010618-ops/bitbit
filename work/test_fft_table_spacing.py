from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parents[1]
BATCH_PDF = ROOT / 'outputs' / 'DSP讲义重制_第八批_原PPT228-265页_FFT_手绘复刻版.pdf'


def test_fft_warning_has_clear_gap_below_operation_table():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[0]
        table_bottom = max(
            rect['bottom']
            for rect in page.rects
            if rect['x0'] <= 49 and rect['x1'] >= 557 and 250 < rect['top'] < 340
        )
        warning_top = min(
            word['top']
            for word in page.extract_words()
            if word['text'] == 'FFT' and word['x0'] < 55 and word['top'] > table_bottom - 5
        )

    assert warning_top - table_bottom >= 6


def test_split_flow_last_sequence_labels_stay_inside_their_frames():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[1]
        last_labels = [
            word for word in page.extract_words()
            if word['text'] in {'x(7)', 'X(7)'}
        ]
        frames = [
            curve for curve in page.curves
            if curve['height'] > 130 and (curve['x0'] < 100 or curve['x1'] > 500)
        ]

    assert len(last_labels) == 2
    for label in last_labels:
        frame = min(frames, key=lambda item: abs((item['x0'] + item['x1']) / 2 - (label['x0'] + label['x1']) / 2))
        assert label['top'] >= frame['top']
        assert label['bottom'] <= frame['bottom']


def test_split_flow_uses_the_source_single_branch_before_even_odd_paths():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[1]
        branch_lines = [
            line for line in page.lines
            if (
                100 < line['x0'] < 150
                and abs(line['x1'] - line['x0']) < 0.5
                and line['height'] > 70
            )
        ]

    assert branch_lines, 'Missing the source diagram\'s vertical even/odd split branch'


def test_split_flow_sequence_titles_clear_the_frames():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[1]
        frames = [curve for curve in page.curves if curve['height'] > 160]
        input_frame = min(frames, key=lambda curve: curve['x0'])
        output_frame = max(frames, key=lambda curve: curve['x1'])
        input_title = next(word for word in page.extract_words() if word['text'] == 'x(n)')
        output_title = next(
            word for word in page.extract_words()
            if word['text'] == 'X(k)' and word['x0'] > 490
        )

    assert input_title['bottom'] <= input_frame['top'] - 3
    assert output_title['bottom'] <= output_frame['top'] - 3


def test_small_butterfly_has_only_the_two_source_diagonals():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[1]
        butterfly_lines = [
            line for line in page.lines
            if 270 < line['x0'] < 360 and 340 < line['top'] < 440
        ]
        horizontal = [line for line in butterfly_lines if line['height'] < 0.5]
        diagonal = [line for line in butterfly_lines if line['height'] > 40 and line['width'] > 40]

    assert horizontal == []
    assert len(diagonal) == 2


def test_even_odd_labels_sit_on_their_source_branch_paths():
    with pdfplumber.open(BATCH_PDF) as pdf:
        page = pdf.pages[1]
        labels = [
            word for word in page.extract_words()
            if word['text'] in {'偶序号', '奇序号'}
        ]

    assert len(labels) == 2
    assert all(label['x1'] < 150 for label in labels)
    assert all(label['top'] < 260 for label in labels)
