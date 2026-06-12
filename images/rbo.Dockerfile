FROM frappe/erpnext:v16.22.0

USER frappe
WORKDIR /home/frappe/frappe-bench

# Copy rbo custom app
COPY --chown=frappe:frappe apps/rbo apps/rbo

# Add rbo to Python path so it can be imported
RUN echo "/home/frappe/frappe-bench/apps" > env/lib/python3.14/site-packages/rbo.pth
