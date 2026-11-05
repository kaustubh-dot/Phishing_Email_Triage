"""Protocol and indicator regression checks; no models or dataset downloads."""
import asyncio
import json
from pathlib import Path
import sys
import unittest
from datetime import timedelta

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mcp_indicator_server import extract_urls, check_domain_lookalike, extract_sender_headers


class IndicatorTests(unittest.TestCase):
    def test_normalized_urls_preserve_destination_and_query(self):
        text = 'hxxps://paypa1[.]com/login http : / / example . com /x <a href="https://a.example/?a=1&amp;b=2">'
        self.assertEqual(extract_urls(text), [
            'https://paypa1.com/login', 'http://example.com/x', 'https://a.example/?a=1&b=2'])

    def test_actual_host_and_brand_boundary(self):
        deceptive = check_domain_lookalike('https://paypal.com@evil.example/login')
        self.assertEqual(deceptive['host'], 'evil.example')
        self.assertTrue(deceptive['flagged'])
        self.assertTrue(check_domain_lookalike('https://paypal.com.evil.example/')['flagged'])
        self.assertFalse(check_domain_lookalike('https://accounts.google.com/')['flagged'])

    def test_body_cannot_supply_a_sender_header(self):
        self.assertEqual(extract_sender_headers('Hello\n\nFrom: attacker@example.com')['sender_addresses'], [])
        headers = 'From: Alice <a@example.com>\nReply-To: Bob\n <b@example.com>\n\nBody'
        self.assertEqual(extract_sender_headers(headers)['sender_addresses'], ['a@example.com', 'b@example.com'])


class MCPTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_discovery_calls_and_argument_validation(self):
        path = Path(__file__).resolve().parents[1] / 'mcp_indicator_server.py'
        async with asyncio.timeout(20):
            async with stdio_client(StdioServerParameters(command=sys.executable, args=[str(path)])) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=10)) as session:
                    await session.initialize()
                    listing = await session.list_tools()
                    self.assertEqual({t.name for t in listing.tools}, {
                        'extract_urls', 'check_domain_lookalike', 'extract_sender_headers'})
                    for fn, args in [
                        (extract_urls, {'email_text':'hxxps://paypa1[.]com/login'}),
                        (check_domain_lookalike, {'url':'https://paypal.com@evil.example/login'}),
                        (extract_sender_headers, {'email_text':'From: A <a@example.com>\n\nHello'}),
                    ]:
                        result = await session.call_tool(fn.__name__, args)
                        self.assertFalse(result.isError)
                        expected = fn(**args)
                        if result.structuredContent is None:
                            self.assertEqual(json.loads(result.content[0].text), expected)
                        else:
                            self.assertEqual(result.structuredContent, {'result':expected})
                    invalid = await session.call_tool('extract_urls', {'email_text':42})
                    self.assertTrue(invalid.isError)


if __name__ == '__main__':
    unittest.main()
