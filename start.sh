#!/bin/bash
set -e

echo "=========================================="
echo "  Ritam Bharat OS - Setup"
echo "=========================================="

PROJECT=$(basename "$PWD")

# Build custom Docker image with rbo app
echo ""
echo "[1/3] Building Docker image..."
docker buildx build --load \
  -t ritam-bharat-os:v1.0 \
  -f images/rbo.Dockerfile .
echo "  ✅ Image built"

# Start containers
echo ""
echo "[2/3] Starting containers..."
docker compose -f compose.yaml \
  -f overrides/compose.mariadb.yaml \
  -f overrides/compose.redis.yaml \
  -f overrides/compose.local.yaml \
  up -d
echo "  ✅ Containers started"

# Wait for backend to be ready
echo ""
echo "[3/3] Creating site..."
sleep 10

BACKEND=$(docker compose ps -q backend 2>/dev/null || echo "")

create_site() {
  docker compose exec -T backend \
    bench new-site os.localhost \
    --mariadb-root-password ritam@123 \
    --db-host db \
    --admin-password admin \
    --install-app erpnext 2>/dev/null || true
}

install_rbo() {
  docker compose exec -T backend \
    bench --site os.localhost install-app rbo
}

setup_branding() {
  docker compose exec -T backend \
    bash -c 'cd /home/frappe/frappe-bench && bench --site os.localhost console <<EOF
frappe.db.set_value("System Settings", None, "setup_completed", 1)
frappe.db.set_value("System Settings", None, "language", "en")
frappe.db.set_value("System Settings", None, "time_zone", "Asia/Kolkata")
frappe.db.set_value("System Settings", None, "country", "India")
frappe.db.set_value("System Settings", None, "currency", "INR")
frappe.db.set_value("System Settings", None, "app_name", "Ritam Bharat OS")
frappe.db.set_value("Website Settings", None, "app_name", "Ritam Bharat OS")
frappe.db.commit()
exit()
EOF' | tail -1
}

create_site
install_rbo
setup_branding

echo ""
echo "=========================================="
echo "  ✅ Ritam Bharat OS is ready!"
echo "  URL: http://localhost:8080"
echo "  Login: administrator / admin"
echo "=========================================="
