FROM frappe/erpnext:v16.22.0

USER frappe
WORKDIR /home/frappe/frappe-bench

COPY --chown=frappe:frappe apps/rbo apps/rbo
RUN echo "/home/frappe/frappe-bench/apps" > env/lib/python3.14/site-packages/rbo.pth

# Copy rbo assets directly into the served assets directory
RUN mkdir -p assets/rbo && cp -r apps/rbo/public/* assets/rbo/
