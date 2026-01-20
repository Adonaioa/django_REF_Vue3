import csv
import io
from datetime import date
from typing import Iterable, Tuple, Union

import pandas as pd
from rest_framework.pagination import PageNumberPagination


def _success(data=None, message: str = "success"):
    return {"code": 200, "message": message, "data": data}


def _error(message: str = "error", code: int = 400):
    return {"code": code, "message": message, "data": None}


def _to_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_date(value) -> date:
    if not value:
        return date.today()
    try:
        return date.fromisoformat(str(value)[:10])
    except Exception:
        return date.today()


def _read_upload_rows(upload) -> Tuple[Union[Iterable[dict], None], Union[str, None]]:
    name = (upload.name or "").lower()
    df = None

    if name.endswith(".csv"):
        for enc in ["utf-8-sig", "gbk", None]:
            upload.file.seek(0)
            try:
                df = pd.read_csv(upload.file, encoding=enc or "utf-8", engine="python")
                break
            except UnicodeDecodeError:
                continue
            except Exception:
                continue
        if df is None:
            return None, "CSV 解析失败，请确认编码为 UTF-8/GBK"

    elif name.endswith(".xlsx"):
        upload.file.seek(0)
        try:
            df = pd.read_excel(upload.file, engine="openpyxl")
        except ImportError:
            return None, "缺少 openpyxl，请安装后再试"
        except Exception:
            return None, "Excel 解析失败，请确认文件未损坏"

    elif name.endswith(".xls"):
        upload.file.seek(0)
        try:
            df = pd.read_excel(upload.file, engine="xlrd")
        except ImportError:
            return None, "缺少 xlrd==1.2.0，请安装后再试，或另存为 xlsx/csv"
        except Exception:
            return None, "Excel 解析失败，请确认文件未损坏"

    else:
        return None, "仅支持 csv、xlsx、xls 文件"

    if df is None:
        return None, "文件读取失败"

    df = df.rename(columns=lambda c: str(c).strip())
    df = df.fillna("")
    return df.to_dict(orient="records"), None


class _Page(PageNumberPagination):
    page_size_query_param = "size"
    page_query_param = "page"
