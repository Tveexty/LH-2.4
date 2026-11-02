#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый IPC-клиент для проверки ядра Luma Beta (Luma_Core/test_ipc_client.py).
Подключается к 127.0.0.1:45890 (или поднимает временный сокет) и проверяет:
  1. {"jsonrpc": "2.0", "method": "system.ping", "id": 1}
  2. {"jsonrpc": "2.0", "method": "widgets.list", "id": 2}
  3. {"method": "widgets.get_data"}
"""

import asyncio
import json
from luma_core import LumaCoreServer


async def main() -> None:
    server = LumaCoreServer(host="127.0.0.1", port=45891)
    server.metrics.start()
    tcp_srv = await asyncio.start_server(server._handle_client, "127.0.0.1", 45891)

    async with tcp_srv:
        reader, writer = await asyncio.open_connection("127.0.0.1", 45891)
        requests = [
            '{"jsonrpc": "2.0", "method": "system.ping", "id": 1}',
            '{"jsonrpc": "2.0", "method": "widgets.list", "id": 2}',
            '{"method": "widgets.get_data"}',
            '{"jsonrpc": "2.0", "method": "system.info", "id": 4}',
        ]
        for req in requests:
            print(f"\n[CLIENT -> CORE] {req}")
            writer.write((req + "\n").encode("utf-8"))
            await writer.drain()
            resp_line = await reader.readline()
            parsed = json.loads(resp_line.decode("utf-8"))
            print(f"[CORE -> CLIENT] {json.dumps(parsed, ensure_ascii=False, indent=2)}")

        writer.close()
        await writer.wait_closed()
        await server.metrics.stop()


if __name__ == "__main__":
    asyncio.run(main())
