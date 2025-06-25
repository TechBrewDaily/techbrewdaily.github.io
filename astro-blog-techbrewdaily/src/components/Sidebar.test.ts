const { render, screen } = require('@testing-library/vue');
const Sidebar = require('./Sidebar.astro');

test('renders recent posts', async () => {
    const recentPosts = [
        { id: '1', data: { title: 'Post 1', pubDate: new Date() } },
        { id: '2', data: { title: 'Post 2', pubDate: new Date() } },
    ];
    render(Sidebar, { props: { recentPosts } });
    expect(screen.getByText('Recent Posts')).toBeInTheDocument();
    expect(screen.getByText('Post 1')).toBeInTheDocument();
    expect(screen.getByText('Post 2')).toBeInTheDocument();
});

test('renders categories', async () => {
    const categories = [
        { name: 'Web Development', count: 8 },
        { name: 'AI & Machine Learning', count: 12 },
    ];
    render(Sidebar, { props: { categories } });
    expect(screen.getByText('Categories')).toBeInTheDocument();
    expect(screen.getByText('Web Development')).toBeInTheDocument();
    expect(screen.getByText('AI & Machine Learning')).toBeInTheDocument();
});

test('renders newsletter signup', async () => {
    render(Sidebar);
    expect(screen.getByText('Stay Updated')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Your email')).toBeInTheDocument();
});