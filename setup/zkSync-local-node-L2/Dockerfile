# Use the matterlabs/geth image as the base
FROM matterlabs/geth

# Copy your custom geth-entry.sh script into the container
COPY geth-entry.sh /bin/geth-entry.sh

# Make sure the script is executable
RUN chmod +x /bin/geth-entry.sh

# Optional: specify the default command or entrypoint if needed
# ENTRYPOINT ["/bin/geth-entry.sh"]
