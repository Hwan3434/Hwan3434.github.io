const { McpServer } = require("@modelcontextprotocol/sdk/server/mcp.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { z } = require("zod");
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const BLOG_DIR = path.resolve(__dirname, '..');

function runGit(args) {
    try {
        return execFileSync('git', args, { cwd: BLOG_DIR, encoding: 'utf-8' });
    } catch (e) {
        throw new Error(`Git error: ${e.stderr || e.message}`);
    }
}

const server = new McpServer({
    name: "Blog Manager",
    version: "1.0.0"
});

server.tool(
    "create_blog_post",
    {
        title: z.string().describe("The title of the blog post"),
        content: z.string().describe("The main markdown content"),
        category: z.string().default("etc").describe("Category folder (e.g. news, tech, philosophy)"),
        slug: z.string().optional().describe("Optional english slug for the filename. If not provided, a default one is generated.")
    },
    async ({ title, content, category, slug }) => {
        let finalSlug = slug;
        if (!finalSlug) {
            finalSlug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
            if (!finalSlug) {
                finalSlug = `post-${Date.now()}`;
            }
        }

        const now = new Date();
        const kstOffset = 9 * 60 * 60 * 1000;
        const kst = new Date(now.getTime() + kstOffset);
        
        const pad = n => n.toString().padStart(2, '0');
        const dateStr = `${kst.getUTCFullYear()}-${pad(kst.getUTCMonth()+1)}-${pad(kst.getUTCDate())}`;
        const timeStr = `${pad(kst.getUTCHours())}:${pad(kst.getUTCMinutes())}:${pad(kst.getUTCSeconds())}`;
        const datetimeStr = `${dateStr} ${timeStr} +0900`;

        const filename = `${dateStr}-${finalSlug}.md`;
        const catLower = category.toLowerCase();
        
        const outDir = path.join(BLOG_DIR, '_posts', catLower);
        if (!fs.existsSync(outDir)) {
            fs.mkdirSync(outDir, { recursive: true });
        }

        const outPath = path.join(outDir, filename);
        
        const frontmatter = `---\nlayout: post\ntitle: "${title}"\ndate: ${datetimeStr}\ncategories: [${catLower}]\n---\n\n`;
        
        fs.writeFileSync(outPath, frontmatter + content, 'utf-8');

        runGit(['add', outPath]);
        runGit(['commit', '-m', `docs: add new post '${title}'`]);
        runGit(['push']);

        return {
            content: [{ type: "text", text: `Successfully created and published blog post: ${outPath}` }]
        };
    }
);

server.tool(
    "list_blog_categories",
    {},
    async () => {
        const postsDir = path.join(BLOG_DIR, '_posts');
        if (!fs.existsSync(postsDir)) {
            return { content: [{ type: "text", text: "No categories found." }] };
        }
        
        const items = fs.readdirSync(postsDir, { withFileTypes: true });
        const categories = items.filter(d => d.isDirectory()).map(d => d.name);
        
        return {
            content: [{ type: "text", text: `Existing categories: ${categories.join(', ')}` }]
        };
    }
);

async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

main().catch(console.error);
