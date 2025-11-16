import re
from typing import List, Dict, Any, Optional, Tuple

def cleaned_address(data: List[Dict]) -> List[Dict]:
    """
    Clean address data từ list of dictionaries
    """
    result = []
    
    for item in data:
        new_item = item.copy()
        
        # 1. Xử lý "Address" (có thể là "address" hoặc "Address" tùy data source)
        address_key = None
        for key in ['Address', 'address']:
            if key in new_item:
                address_key = key
                break
                
        if address_key and new_item.get(address_key):
            address = new_item[address_key]
            # Tách địa chỉ
            parts = address.split(",", 1)
            city = parts[0].strip()
            district = parts[1].strip() if len(parts) > 1 else ""
            
            # Chuẩn hóa tên thành phố
            city_map = {
                "Hồ Chí Minh": "TP. Hồ Chí Minh",
                "Ho Chi Minh": "TP. Hồ Chí Minh",
                "TP HCM": "TP. Hồ Chí Minh",
                "Hà Nội": "Hà Nội",
                "Ha Noi": "Hà Nội",
            }
            
            if city in city_map:
                city = city_map[city]
                
            new_item["City"] = city
            new_item["District"] = district
            
            # Xóa cột address gốc nếu muốn
            # del new_item[address_key]
        
        # 2. Xử lý "Detail Address" (làm sạch định dạng)
        detail_addr_keys = ['Detail Address', 'detail_address', 'working_addresses']
        detail_addr_key = None
        for key in detail_addr_keys:
            if key in new_item:
                detail_addr_key = key
                break
                
        if detail_addr_key and new_item.get(detail_addr_key):
            detail_addr = new_item[detail_addr_key] or ""
            # Làm sạch định dạng
            cleaned_addr = re.sub(r"^[\s\-–—]+", "", detail_addr)
            cleaned_addr = re.sub(r";\s*[\-–—]+\s*", "; ", cleaned_addr)
            new_item[detail_addr_key] = cleaned_addr.strip()
        
        result.append(new_item)
    
    return result

def cleaned_salary(salary_text: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    """
    Clean salary text và trả về (min_salary, max_salary)
    """
    if not salary_text:
        return None, None
        
    s = str(salary_text).lower().strip()

    # Bỏ chữ 'triệu', 'tr' và chuẩn hóa dấu gạch
    s = (s.replace("triệu", "")
          .replace("tr", "")
          .replace("–", "-")
          .replace("—", "-")
          .strip())

    # 1) dạng "25 - 28"
    m = re.search(r"(\d+)\s*-\s*(\d+)", s)
    if m:
        low = float(m.group(1))
        high = float(m.group(2))
        return low, high

    # 2) dạng "tới 25", "đến 25"
    m = re.search(r"(tới|đến|toi|den)\s*(\d+)", s)
    if m:
        high = float(m.group(2))
        return 0.0, high   # hiểu là 0–25

    # 3) dạng "25 triệu" / "25"
    m = re.search(r"(\d+)", s)
    if m:
        val = float(m.group(1))
        return val, val

    # 4) "Thoả thuận" hoặc không parse được -> None
    return None, None

def transform_data_cleaned(data: List[Dict]) -> List[Dict]:
    """
    Transform và clean data từ list of dictionaries
    """
    # 1. Clean address
    data = cleaned_address(data)
    
    # 2. Clean salary
    for item in data:
        # Tìm key salary (có thể có nhiều tên khác nhau)
        salary_keys = ['Salary (Triệu VND)', 'salary', 'salary_list']
        salary_key = None
        for key in salary_keys:
            if key in item:
                salary_key = key
                break
                
        if salary_key:
            salary_text = item[salary_key]
            min_salary, max_salary = cleaned_salary(salary_text)
            
            item["Min Salary"] = min_salary
            item["Max Salary"] = max_salary
            
            # Tính salary trung bình
            if min_salary is not None and max_salary is not None:
                item["Salary_Avg"] = (min_salary + max_salary) / 2
            elif min_salary is not None:
                item["Salary_Avg"] = min_salary
            elif max_salary is not None:
                item["Salary_Avg"] = max_salary
            else:
                item["Salary_Avg"] = None
    
    # 3. Remove duplicates based on Job URL
    seen_urls = set()
    unique_data = []
    
    for item in data:
        url_keys = ['Job URL', 'job_url', 'url']
        url = None
        for key in url_keys:
            if key in item:
                url = item[key]
                break
                
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_data.append(item)
        elif not url:  # Nếu không có URL, vẫn giữ lại
            unique_data.append(item)
    
    return unique_data

