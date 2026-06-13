FROM frappe/erpnext:v16.22.0

USER frappe
WORKDIR /home/frappe/frappe-bench

COPY --chown=frappe:frappe apps/rbo apps/rbo
RUN echo "/home/frappe/frappe-bench/apps" > env/lib/python3.14/site-packages/rbo.pth

# Install India Compliance app for GST
RUN bench get-app --branch version-16 india_compliance https://github.com/resilient-tech/india-compliance.git

# Copy rbo assets directly into the served assets directory
RUN mkdir -p assets/rbo && cp -r apps/rbo/public/* assets/rbo/
