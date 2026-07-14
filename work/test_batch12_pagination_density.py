from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "outputs" / "DSP讲义重制_第十二批_原PPT367-399页_FIR滤波器设计_手绘复刻版.pdf"


def _page_text(index: int) -> str:
    return PdfReader(PDF).pages[index].extract_text() or ""


def _page_containing(fragment: str) -> str:
    for page in PdfReader(PDF).pages:
        text = page.extract_text() or ""
        if fragment in text:
            return text
    raise AssertionError(f"No page contains {fragment!r}")


def test_zero_analysis_continues_after_classification_without_forced_blank_page():
    page = _page_text(0)
    assert "6.4.3 线性相位 FIR 系统函数零点特点" in page
    assert "由 z 变换表达式和线性相位条件分析零点" in page


def test_bandpass_content_flows_after_lowpass_and_highpass_when_space_allows():
    page = _page_containing("6.5.1 线性相位 FIR 理想滤波器")
    assert "1. 理想低通滤波器" in page
    assert "2. 理想高通滤波器" in page
    assert "3. 理想带通滤波器" in page


def test_window_method_starts_below_ideal_response_plots_instead_of_leaving_blank_page_tail():
    page = _page_containing("四类理想频率响应与冲激响应")
    assert "6.5.2 利用窗函数法设计 FIR 滤波器" in page
