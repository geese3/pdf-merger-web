import os
import tempfile
import uuid
import io
from pathlib import Path
from typing import List, Optional
import logging

try:
    from PyPDF2 import PdfMerger
except ImportError as e:
    print(f"필요한 라이브러리가 설치되지 않았습니다: {e}")
    print("pip install PyPDF2를 실행해주세요.")
    exit(1)

class PDFMergerWeb:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def merge_pdfs(
        self,
        pdf_files: List[str],
        output_filename: Optional[str] = None
    ) -> str:
        """
        여러 PDF 파일을 하나로 병합
        
        Args:
            pdf_files: 병합할 PDF 파일 경로 리스트
            output_filename: 결과 파일명 (None이면 자동 생성)
            
        Returns:
            병합된 PDF 파일 경로
        """
        if not pdf_files:
            raise ValueError("병합할 PDF 파일이 없습니다.")
        
        # 출력 파일명 생성
        if not output_filename:
            output_filename = f"merged_{uuid.uuid4().hex[:8]}.pdf"
        
        # 임시 디렉토리에 결과 파일 저장
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, output_filename)
        
        merger = PdfMerger()
        
        try:
            # 각 PDF 파일을 순차적으로 병합
            for pdf_path in pdf_files:
                if not os.path.exists(pdf_path):
                    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")
                
                self.logger.info(f"병합 중: {os.path.basename(pdf_path)}")
                merger.append(pdf_path)
            
            # 결과 파일 저장
            merger.write(output_path)
            merger.close()
            
            self.logger.info(f"PDF 병합 완료: {output_path}")
            return output_path
            
        except Exception as e:
            merger.close()
            self.logger.error(f"PDF 병합 중 오류 발생: {str(e)}")
            raise e

    def get_pdf_info(self, pdf_path: str) -> dict:
        """
        PDF 파일 정보 가져오기
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            PDF 정보 딕셔너리
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_data = file.read()
            
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(pdf_data))
            
            info = {
                'page_count': len(reader.pages),
                'title': reader.metadata.get('/Title', ''),
                'author': reader.metadata.get('/Author', ''),
                'subject': reader.metadata.get('/Subject', ''),
                'creator': reader.metadata.get('/Creator', ''),
                'producer': reader.metadata.get('/Producer', ''),
                'file_size': os.path.getsize(pdf_path)
            }
            
            return info
                
        except Exception as e:
            self.logger.error(f"PDF 정보 읽기 중 오류: {str(e)}")
            return {
                'page_count': 0,
                'title': '',
                'author': '',
                'subject': '',
                'creator': '',
                'producer': '',
                'file_size': 0
            }

    def split_pdf(
        self,
        pdf_path: str,
        page_ranges: List[tuple],
        output_filename_prefix: Optional[str] = None
    ) -> List[str]:
        """
        PDF 파일을 페이지 범위에 따라 분리
        
        Args:
            pdf_path: 분리할 PDF 파일 경로
            page_ranges: 페이지 범위 리스트 [(시작, 끝), ...]
            output_filename_prefix: 출력 파일명 접두사 (None이면 자동 생성)
            
        Returns:
            분리된 PDF 파일 경로 리스트
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pdf_path}")
        
        # 출력 파일명 접두사 생성
        if not output_filename_prefix:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename_prefix = f"{base_name}_split"
        
        # 임시 디렉토리에 결과 파일 저장
        temp_dir = tempfile.mkdtemp()
        output_files = []
        
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            # PDF 파일 읽기 - 파일을 메모리에 완전히 로드
            with open(pdf_path, 'rb') as file:
                pdf_data = file.read()
            
            # PDF 데이터로부터 reader 생성
            reader = PdfReader(io.BytesIO(pdf_data))
            total_pages = len(reader.pages)
            
            # 각 범위별로 PDF 파일 생성
            for i, (start, end) in enumerate(page_ranges):
                if start < 1 or end > total_pages or start > end:
                    raise ValueError(f"잘못된 페이지 범위: {start}-{end} (총 {total_pages}페이지)")
                
                writer = PdfWriter()
                for page_num in range(start, end + 1):
                    writer.add_page(reader.pages[page_num - 1])
                
                # 출력 파일명 생성
                if start == end:
                    output_filename = f"{output_filename_prefix}_page_{start}.pdf"
                else:
                    output_filename = f"{output_filename_prefix}_pages_{start}-{end}.pdf"
                
                output_path = os.path.join(temp_dir, output_filename)
                
                # 파일 저장
                with open(output_path, "wb") as output:
                    writer.write(output)
                
                output_files.append(output_path)
                self.logger.info(f"PDF 분리 완료: {output_filename}")
            
            return output_files
            
        except Exception as e:
            self.logger.error(f"PDF 분리 중 오류 발생: {str(e)}")
            raise e

    def parse_page_ranges(self, page_range_str: str, total_pages: int) -> List[tuple]:
        """
        페이지 범위 문자열을 파싱
        
        Args:
            page_range_str: 페이지 범위 문자열 (예: "1-3,5,7-9")
            total_pages: 총 페이지 수
            
        Returns:
            페이지 범위 리스트 [(시작, 끝), ...]
        """
        try:
            ranges = []
            parts = page_range_str.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if 1 <= start <= end <= total_pages:
                        ranges.append((start, end))
                    else:
                        raise ValueError(f"잘못된 페이지 범위: {start}-{end}")
                else:
                    try:
                        page = int(part)
                        if 1 <= page <= total_pages:
                            ranges.append((page, page))
                        else:
                            raise ValueError(f"잘못된 페이지 번호: {page}")
                    except ValueError:
                        raise ValueError(f"잘못된 페이지 형식: {part}")
            
            return ranges
            
        except Exception as e:
            self.logger.error(f"페이지 범위 파싱 오류: {str(e)}")
            raise e

    def cleanup_temp_files(self, file_paths: List[str]):
        """
        임시 파일 정리
        
        Args:
            file_paths: 삭제할 파일 경로 리스트
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.logger.info(f"임시 파일 삭제: {file_path}")
            except Exception as e:
                self.logger.warning(f"임시 파일 삭제 실패: {file_path} - {str(e)}")
