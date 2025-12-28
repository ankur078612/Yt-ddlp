import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
    const searchParams = request.nextUrl.searchParams;
    const mobile = searchParams.get('mobile');
    const email = searchParams.get('email');

    const baseUrl = process.env.API_BASE_URL;

    if (!baseUrl) {
        console.error("API_BASE_URL is not defined");
        return NextResponse.json({ error: "Configuration Error" }, { status: 500 });
    }

    const url = new URL(baseUrl);

    if (mobile) {
        url.searchParams.append('mobile', mobile);
    }
    if (email) {
        url.searchParams.append('email', email);
    }

    try {
        // Simplified proxy: forward request to external API and return its JSON.
        const response = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (compatible; LeakDataChecker/1.0)',
            },
        });

        if (!response.ok) {
            return NextResponse.json({ error: `External API error: ${response.status}` }, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error("Proxy Error:", error);
        return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
    }
}
