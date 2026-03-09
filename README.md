# 📚 Bookstore Microservices

Hệ thống quản lý Thư viện / Cửa hàng sách trực tuyến được xây dựng theo kiến trúc Microservices hiện đại, sử dụng Python (Django framework) và được đóng gói toàn bộ qua Docker.

## 🏗 Cấu trúc hệ thống

Dự án được ứng dụng mô hình Microservices, tách biệt hoàn toàn giữa Frontend và Backend. Cấu trúc được chia thành các dịch vụ chính:

1. **Frontend Service** (`frontend-service`): Chịu trách nhiệm hiển thị giao diện UI (HTML/CSS) cho người dùng.
2. **API Gateway** (`api_gateway`): Đóng vai trò là cửa ngõ giao tiếp tập trung phân phối mọi Request API xuống các Microservices bên dưới.
3. **Các Microservices nghiệp vụ** (Core Services): Xử lý logic cụ thể của từng chức năng độc lập (Book, Customer, Cart, Order, Staff, Manager...).

### 🔌 Danh sách các cổng (Ports) đang chạy

- **🌐 Frontend Web App:** `http://localhost:3000`
- **🚪 API Gateway:** `http://localhost:8000` (Gọi API với tiền tố `/api/`)
- Các dịch vụ nội bộ (Gọi từ Gateway qua, không cần gọi trực tiếp mở màng ngoài):
  - `customer-service`: 8001
  - `book-service`: 8002
  - `cart-service`: 8003
  - `staff-service`: 8004
  - `manager-service`: 8005
  - `catalog-service`: 8006
  - `order-service`: 8007
  - `ship-service`: 8008
  - `pay-service`: 8009
  - `comment-rate-service`: 8010
  - `recommender-ai-service`: 8011

---

## 🚀 Hướng dẫn cài đặt và chạy dự án

Đảm bảo bạn đã cài đặt **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** trên máy của mình trước khi bắt đầu. Bạn cũng cần bật (Khởi động) Docker hoạt động (biểu tượng cá voi màu xanh/trạng thái Engine Running).

### Bước 1: Khởi động hệ thống bằng Docker Compose

Mở Terminal / Command Prompt / PowerShell ở thư mục gốc của dự án (nơi chứa file `docker-compose.yml`) và chạy câu lệnh sau:

```bash
docker-compose up -d --build
```

**Giải thích:**

- `up`: Lệnh khởi tạo và chạy các container.
- `-d`: Chạy ngầm (detached mode) để không bị treo Terminal.
- `--build`: Tiến hành build (đóng gói) lại mã nguồn mới nhất của tất cả các image.

### Bước 2: Kiểm tra trạng thái chạy

Sau khi lệnh trên hoàn tất, bạn có thể kiểm tra xem toàn bộ các services đã sáng đèn hay chưa bằng lệnh:

```bash
docker-compose ps
```

### Bước 3: Trải nghiệm ứng dụng

- Mở trình duyệt web và truy cập vào Frontend để xem giao diện:  
  👉 **http://localhost:3000**
- Test thử tập REST API thông qua API Gateway:  
  👉 **http://localhost:8000/api/books/**

---

## 🛠 Cách dừng hệ thống (Tắt Server)

Khi không muốn chạy dự án nữa và giải phóng RAM, bạn sử dụng lệnh:

```bash
docker-compose down
```

Nếu muốn xóa luôn cả data cũ để làm mới database:

```bash
docker-compose down -v
```

---
