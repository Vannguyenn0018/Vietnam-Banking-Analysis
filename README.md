# [cite_start]🏦 Dự án Vietnam-Banking-Analysis: Đánh giá Hiệu quả và Tiềm năng Tăng trưởng Hệ thống Ngân hàng Thương mại Việt Nam (2020-2024) [cite: 6, 7]

## 📖 Tổng quan Dự án
[cite_start]Dự án này được thực hiện trong khuôn khổ Vòng 2 cuộc thi G'CONTEST 2026 bởi đội FINOVA[cite: 8, 13]. [cite_start]Mục tiêu chính là phân tích, đánh giá hiệu quả hoạt động và định vị tiềm năng tăng trưởng của hệ thống ngân hàng Việt Nam trong giai đoạn 5 năm đầy biến động từ 2020 đến 2024[cite: 4, 5, 6]. [cite_start]Bằng việc ứng dụng các phương pháp phân tích dữ liệu nâng cao, dự án cung cấp góc nhìn đa chiều về rủi ro, khả năng sinh lời và đưa ra các đề xuất chiến lược[cite: 1121, 1132].

## 📊 Mô tả Dữ liệu
* [cite_start]**Quy mô:** 27 Ngân hàng Thương mại tại Việt Nam[cite: 2, 7].
* [cite_start]**Đặc trưng:** 272 biến số tài chính và vĩ mô[cite: 9].
* [cite_start]**Giai đoạn:** Dữ liệu chuỗi thời gian từ năm 2020 đến 2024[cite: 4].

## 🛠 Cấu trúc Phân tích & Kỹ thuật áp dụng
Dự án được thiết kế theo quy trình phân tích từ mô tả đến chẩn đoán và dự báo:

* [cite_start]**Descriptive Analytics:** Trực quan hóa xu hướng của Tổng tài sản, Cho vay khách hàng, Tiền gửi, Biên lãi thuần (NIM), LDR và tỷ lệ Nợ xấu (NPL)[cite: 10, 64, 65, 74].
* [cite_start]**Diagnostic Analytics:** Bóc tách các động lực tăng trưởng cốt lõi và phân tích sâu các yếu tố làm biến động lợi nhuận sau thuế của toàn hệ thống[cite: 11, 40, 255].
* [cite_start]**Machine Learning - K-Means Clustering:** Áp dụng thuật toán K-Means để phân cụm 27 ngân hàng thành 3 nhóm đặc trưng (Big4, Large, Small) dựa trên 3 biến trọng yếu là Tổng tài sản, Cho vay và Tiền gửi[cite: 326, 421].
* [cite_start]**Machine Learning - PCA (Principal Component Analysis):** Giảm chiều dữ liệu từ 5 biến vĩ mô xuống 2 thành phần chính (PC1: Hiệu quả tài chính & Sức mạnh huy động, PC2: Rủi ro tín dụng) nhằm xây dựng ma trận nhận diện vị thế ngân hàng[cite: 1027, 1028, 1045].
* [cite_start]**Mô hình Hồi quy OLS:** Đánh giá độ nhạy của các biến vĩ mô (Cung tiền M2, FDI, tỷ giá USD/VND) đối với tỷ lệ ROA và NPL[cite: 855, 856].

## 💡 Key Findings (Điểm nhấn Insight)
* [cite_start]**Biến động NIM & NPL:** NIM toàn hệ thống đạt đỉnh 3.75% vào năm 2022 nhưng thu hẹp lại trong năm 2023, song song đó NPL cũng chạm mốc cao nhất vào 2023 trước khi có dấu hiệu hạ nhiệt vào 2024 nhờ các nỗ lực xử lý nợ[cite: 237, 241, 700, 705].
* [cite_start]**Sức mạnh của CASA:** Mô hình ma trận đã chỉ ra mối tương quan thuận mạnh mẽ giữa tỷ trọng tiền gửi không kỳ hạn (CASA) và Biên lãi thuần (NIM) tối ưu[cite: 714]. [cite_start]Đáng chú ý, nhóm Big 4 đã cải thiện vượt bậc và vươn lên dẫn đầu về tỷ lệ CASA vào năm 2024[cite: 750, 852].
* [cite_start]**Nút thắt trong mô hình Vĩ mô:** Phân tích OLS cho thấy hiện tượng đa cộng tuyến nghiêm trọng giữa tỷ giá USD/VND và FDI, đồng thời khẳng định Quy mô ngân hàng (Cluster Effect) mới là yếu tố nội tại chính giải thích cho sự chênh lệch ROA, thay vì chỉ dựa vào biến động vĩ mô[cite: 860, 864, 897].
* [cite_start]**Phân hóa Ngành sâu sắc:** Nhóm Large Banks tiếp tục duy trì ưu thế nhờ CASA và danh mục bán lẻ, trong khi Small Banks đối mặt với áp lực lớn từ rủi ro nợ xấu gia tăng và hiệu quả sinh lời trên tài sản (ROA) ngày càng thu hẹp[cite: 355, 403, 489, 1023].

## 🚀 Đề xuất Chiến lược
* [cite_start]Đẩy mạnh chuyển đổi số và ứng dụng AI/ML để tối ưu hóa trải nghiệm khách hàng và giảm chi phí vận hành[cite: 1121, 1124, 1128].
* [cite_start]Đa dạng hóa nguồn thu nhập ngoài lãi (phí dịch vụ, bảo hiểm, thanh toán) nhằm giảm bớt sự phụ thuộc vào NIM truyền thống[cite: 1134, 1135].
* [cite_start]Tích hợp sâu sắc các tiêu chuẩn Phát triển Bền vững & ESG vào hoạt động cấp tín dụng và vận hành[cite: 1148, 1150].
* [cite_start]Giải quyết triệt để vấn đề nhiễu và ánh xạ dữ liệu (mapping errors) để củng cố độ chính xác cho các hệ thống cảnh báo rủi ro sớm[cite: 1158, 1162, 1166].
