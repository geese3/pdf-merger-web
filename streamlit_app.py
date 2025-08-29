import streamlit as st
import os
import tempfile
from pathlib import Path
from pdf_merger_web import PDFMergerWeb

# 페이지 설정
st.set_page_config(
    page_title="PDF Merger (Web)",
    page_icon="📄",
    layout="wide"
)

# 제목
st.title("📄 PDF 도구")
st.markdown("**설치 없이 바로 사용할 수 있는 PDF 병합/분리 도구입니다!**")

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 작업 설정")
    
    # 작업 모드 선택
    operation_mode = st.selectbox(
        "작업 모드",
        ["병합", "분리"],
        help="PDF 파일을 병합하거나 분리할 수 있습니다"
    )
    
    if operation_mode == "병합":
        # 병합 설정
        st.subheader("📄 병합 설정")
        
        # 결과 파일명 설정
        output_filename = st.text_input(
            "결과 파일명",
            value="merged.pdf",
            help="병합된 PDF 파일의 이름을 입력하세요"
        )
        
        # 파일 순서 변경 옵션
        st.subheader("📋 파일 순서")
        st.info("파일을 드래그하여 순서를 변경할 수 있습니다.")
    
    elif operation_mode == "분리":
        # 분리 설정
        st.subheader("✂️ 분리 설정")
        
        # 출력 파일명 접두사 설정
        output_filename_prefix = st.text_input(
            "출력 파일명 접두사",
            value="split",
            help="분리된 PDF 파일들의 이름 접두사를 입력하세요"
        )
        
        # 페이지 범위 입력
        st.subheader("📄 페이지 범위")
        st.info("분리할 페이지 범위를 입력하세요 (예: 1-3,5,7-9)\n빈 값으로 두면 모든 페이지를 개별적으로 분리합니다.")
        
        page_range_input = st.text_input(
            "페이지 범위",
            placeholder="1-3,5,7-9 (빈 값 = 모든 페이지 개별 분리)",
            help="쉼표로 구분하여 페이지 범위를 입력하세요. 빈 값으로 두면 모든 페이지를 개별적으로 분리합니다."
        )
        
        # 자동 분리 옵션
        auto_split = st.checkbox(
            "자동 분리",
            value=True,
            help="페이지 범위를 입력했을 때, 선택하지 않은 나머지 페이지들을 자동으로 분리합니다"
        )

# 메인 영역
col1, col2 = st.columns([2, 1])

with col1:
    if operation_mode == "병합":
        st.subheader("📁 PDF 파일 업로드 (병합)")
        
        uploaded_files = st.file_uploader(
            "PDF 파일들을 선택하세요 (여러 개 선택 가능)",
            type=['pdf'],
            accept_multiple_files=True,
            help="Ctrl+클릭으로 여러 파일을 선택할 수 있습니다"
        )
    else:  # 분리 모드
        st.subheader("📁 PDF 파일 업로드 (분리)")
        
        uploaded_file = st.file_uploader(
            "분리할 PDF 파일을 선택하세요",
            type=['pdf'],
            help="한 번에 하나의 PDF 파일만 분리할 수 있습니다"
        )

# 세로 구분선 추가
st.markdown("---")

with col2:
    if operation_mode == "병합" and uploaded_files:
        st.subheader("📋 파일 정보")
        
        # 파일 정보 표시
        total_pages = 0
        total_size = 0
        
        for i, file in enumerate(uploaded_files):
            file_size_mb = file.size / 1024 / 1024
            total_size += file_size_mb
            
            st.write(f"**파일 {i+1}:** {file.name}")
            st.write(f"크기: {file_size_mb:.2f} MB")
            
            # 임시 파일로 저장하여 PDF 정보 가져오기
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name
            
            # PDF 정보 가져오기
            merger = PDFMergerWeb()
            pdf_info = merger.get_pdf_info(tmp_file_path)
            total_pages += pdf_info['page_count']
            
            st.write(f"페이지: {pdf_info['page_count']}페이지")
            if pdf_info['title']:
                st.write(f"제목: {pdf_info['title']}")
            
            # 임시 파일 삭제
            os.unlink(tmp_file_path)
            
            st.markdown("---")
        
        # 전체 정보
        st.write(f"**총 파일 수:** {len(uploaded_files)}개")
        st.write(f"**총 페이지 수:** {total_pages}페이지")
        st.write(f"**총 크기:** {total_size:.2f} MB")
    
    elif operation_mode == "분리" and uploaded_file:
        st.subheader("📋 파일 정보")
        
        file_size_mb = uploaded_file.size / 1024 / 1024
        st.write(f"**파일명:** {uploaded_file.name}")
        st.write(f"**크기:** {file_size_mb:.2f} MB")
        
        # 임시 파일로 저장하여 PDF 정보 가져오기
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # PDF 정보 가져오기
        merger = PDFMergerWeb()
        pdf_info = merger.get_pdf_info(tmp_file_path)
        
        st.write(f"**총 페이지 수:** {pdf_info['page_count']}페이지")
        if pdf_info['title']:
            st.write(f"**제목:** {pdf_info['title']}")
        if pdf_info['author']:
            st.write(f"**작성자:** {pdf_info['author']}")
        
        # 임시 파일 삭제
        os.unlink(tmp_file_path)
        
    else:
        st.info("📁 PDF 파일을 업로드해주세요.")

# 작업 실행 섹션
if (operation_mode == "병합" and uploaded_files) or (operation_mode == "분리" and uploaded_file):
    st.subheader("🚀 작업 실행")
    
    if operation_mode == "병합":
        if st.button("📄 PDF 병합하기", type="primary", use_container_width=True):
            with st.spinner("PDF 파일들을 병합하는 중..."):
                try:
                    # 임시 파일들 저장
                    temp_files = []
                    for file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(file.getvalue())
                            temp_files.append(tmp_file.name)
                    
                    # PDF 병합 실행
                    merger = PDFMergerWeb()
                    output_path = merger.merge_pdfs(temp_files, output_filename)
                    
                    # 결과 파일 읽기
                    with open(output_path, "rb") as f:
                        pdf_data = f.read()
                    
                    st.success(f"✅ PDF 병합 완료! 총 {len(uploaded_files)}개 파일이 병합되었습니다.")
                    
                    # 결과 표시
                    st.subheader("📄 병합된 PDF")
                    
                    # 파일 정보
                    result_info = merger.get_pdf_info(output_path)
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.write(f"**결과 파일명:** {output_filename}")
                        st.write(f"**총 페이지 수:** {result_info['page_count']}페이지")
                    
                    with col_info2:
                        st.write(f"**파일 크기:** {result_info['file_size'] / 1024 / 1024:.2f} MB")
                        if result_info['title']:
                            st.write(f"**제목:** {result_info['title']}")
                    
                    # 다운로드 버튼
                    st.download_button(
                        label="📥 병합된 PDF 다운로드",
                        data=pdf_data,
                        file_name=output_filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # 임시 파일 정리
                    merger.cleanup_temp_files(temp_files + [output_path])
                    
                except Exception as e:
                    st.error(f"❌ 병합 중 오류가 발생했습니다: {str(e)}")
                    
                    # 임시 파일 정리
                    try:
                        merger = PDFMergerWeb()
                        merger.cleanup_temp_files(temp_files)
                    except:
                        pass
    
    elif operation_mode == "분리":
        if st.button("✂️ PDF 분리하기", type="primary", use_container_width=True):
            with st.spinner("PDF 파일을 분리하는 중..."):
                try:
                    # 임시 파일 저장
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # PDF 정보 가져오기
                    merger = PDFMergerWeb()
                    pdf_info = merger.get_pdf_info(tmp_file_path)
                    total_pages = pdf_info['page_count']
                    
                    # 페이지 범위 파싱
                    if not page_range_input:
                        # 페이지 범위를 입력하지 않으면 모든 페이지를 개별적으로 분리
                        page_ranges = [(i, i) for i in range(1, total_pages + 1)]
                        st.info(f"📄 페이지 범위를 입력하지 않아 모든 {total_pages}페이지를 개별적으로 분리합니다.")
                    else:
                        page_ranges = merger.parse_page_ranges(page_range_input, total_pages)
                        
                        # 자동 분리 옵션 처리
                        if auto_split:
                            all_pages = set(range(1, total_pages + 1))
                            selected_pages = set()
                            for start, end in page_ranges:
                                selected_pages.update(range(start, end + 1))
                            
                            remaining_pages = sorted(all_pages - selected_pages)
                            if remaining_pages:
                                # 연속된 페이지들을 범위로 그룹화
                                current_range = [remaining_pages[0], remaining_pages[0]]
                                for page in remaining_pages[1:]:
                                    if page == current_range[1] + 1:
                                        current_range[1] = page
                                    else:
                                        page_ranges.append(tuple(current_range))
                                        current_range = [page, page]
                                page_ranges.append(tuple(current_range))
                    
                    # PDF 분리 실행
                    output_files = merger.split_pdf(tmp_file_path, page_ranges, output_filename_prefix)
                    
                    st.success(f"✅ PDF 분리 완료! 총 {len(output_files)}개 파일로 분리되었습니다.")
                    
                    # 결과 표시
                    st.subheader("✂️ 분리된 PDF 파일들")
                    
                    # 각 분리된 파일에 대한 다운로드 버튼 생성
                    for i, output_path in enumerate(output_files):
                        with open(output_path, "rb") as f:
                            pdf_data = f.read()
                        
                        filename = os.path.basename(output_path)
                        
                        # 파일 정보 표시
                        file_info = merger.get_pdf_info(output_path)
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**파일 {i+1}:** {filename}")
                            st.write(f"**페이지 수:** {file_info['page_count']}페이지")
                            st.write(f"**크기:** {file_info['file_size'] / 1024 / 1024:.2f} MB")
                        
                        with col2:
                            st.download_button(
                                label=f"📥 다운로드",
                                data=pdf_data,
                                file_name=filename,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        
                        st.markdown("---")
                    
                    # 임시 파일 정리
                    merger.cleanup_temp_files([tmp_file_path] + output_files)
                    
                except Exception as e:
                    st.error(f"❌ 분리 중 오류가 발생했습니다: {str(e)}")
                    
                    # 임시 파일 정리
                    try:
                        merger = PDFMergerWeb()
                        merger.cleanup_temp_files([tmp_file_path])
                    except:
                        pass

# 하단 정보
st.markdown("---")
st.markdown("""
### 💡 사용 팁
- **병합 모드**: 여러 PDF 파일을 하나로 병합
- **분리 모드**: 페이지 범위를 지정하여 PDF 분리
- **파일 크기**: 최대 200MB까지 업로드 가능합니다
- **파일 형식**: PDF 파일만 지원됩니다
- **자동 분리**: 선택하지 않은 나머지 페이지들을 자동으로 분리
""")

# 푸터
st.markdown("---")
st.markdown("Made with using Streamlit and PyPDF2")
