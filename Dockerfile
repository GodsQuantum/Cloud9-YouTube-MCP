FROM python:3.12-slim

RUN pip install --no-cache-dir "youtube-complete-mcp" "keyrings.alt>=5.0"

COPY server_wrapper.py /opt/youtube-mcp/server_wrapper.py
WORKDIR /opt/youtube-mcp
EXPOSE 8765
CMD ["python", "/opt/youtube-mcp/server_wrapper.py"]
ENV YOUTUBE_MCP_ENFORCE_GUARD=1
LABEL org.opencontainers.image.source="https://github.com/GodsQuantum/Cloud9-YouTube-MCP" \
      org.opencontainers.image.title="Cloud9-YouTube-MCP" \
      org.opencontainers.image.description="97 YouTube MCP tools, IPv4-compatible Google Data API frontend, safe channel guard" \
      org.opencontainers.image.licenses="MIT"
