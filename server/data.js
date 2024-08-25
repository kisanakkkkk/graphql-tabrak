const users = [
  { id: '1', name: 'John Doe', email: 'john@example.com', age: 30, friendIds: ['2', '3'] },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', age: 25, friendIds: ['1', '4'] },
  { id: '3', name: 'Alice Johnson', email: 'alice@example.com', age: 28, friendIds: ['1'] },
  { id: '4', name: 'Bob Brown', email: 'bob@example.com', age: 35, friendIds: ['2'] },
];

const categories = [
  { id: '1', name: 'Technology' },
  { id: '2', name: 'Health' },
  { id: '3', name: 'Travel' },
];

const tags = [
  { id: '1', name: 'JavaScript' },
  { id: '2', name: 'Node.js' },
  { id: '3', name: 'React' },
  { id: '4', name: 'Fitness' },
  { id: '5', name: 'Nutrition' },
  { id: '6', name: 'Adventure' },
  { id: '7', name: 'Lifestyle' },
];

const posts = [
  {
    id: '1',
    title: 'Understanding JavaScript Closures',
    content: 'Closures are a fundamental concept in JavaScript...',
    authorId: '1',
    categoryId: '1',
    tagIds: ['1', '2'],
    commentIds: ['1', '2'],
    createdAt: new Date('2024-01-01'),
  },
  {
    id: '2',
    title: 'The Benefits of a Balanced Diet',
    content: 'A balanced diet is crucial for maintaining good health...',
    authorId: '2',
    categoryId: '2',
    tagIds: ['4', '5'],
    commentIds: ['3', '4'],
    createdAt: new Date('2024-01-02'),
  },
  {
    id: '3',
    title: 'Top Travel Destinations for 2024',
    content: 'Explore the most exciting travel destinations for the upcoming year...',
    authorId: '3',
    categoryId: '3',
    tagIds: ['6', '7'],
    commentIds: ['5'],
    createdAt: new Date('2024-01-03'),
  },
  {
    id: '4',
    title: 'Advanced Node.js Concepts',
    content: 'Dive deeper into Node.js with advanced concepts and techniques...',
    authorId: '1',
    categoryId: '1',
    tagIds: ['2', '3'],
    commentIds: [],
    createdAt: new Date('2024-01-04'),
  },
];

const comments = [
  {
    id: '1',
    content: 'Great explanation of closures!',
    postId: '1',
    authorId: '2',
    replyIds: ['6'],
    createdAt: new Date('2024-01-01T10:00:00'),
  },
  {
    id: '2',
    content: 'I struggled with closures, but this helped a lot.',
    postId: '1',
    authorId: '3',
    replyIds: [],
    createdAt: new Date('2024-01-01T11:00:00'),
  },
  {
    id: '3',
    content: 'Good advice on diet!',
    postId: '2',
    authorId: '1',
    replyIds: [],
    createdAt: new Date('2024-01-02T10:00:00'),
  },
  {
    id: '4',
    content: 'This is really helpful, thanks for sharing!',
    postId: '2',
    authorId: '4',
    replyIds: ['7'],
    createdAt: new Date('2024-01-02T11:00:00'),
  },
  {
    id: '5',
    content: 'I want to visit all these places!',
    postId: '3',
    authorId: '2',
    replyIds: [],
    createdAt: new Date('2024-01-03T10:00:00'),
  },
  {
    id: '6',
    content: 'Thanks! Glad you found it useful.',
    postId: '1',
    authorId: '1',
    replyIds: [],
    createdAt: new Date('2024-01-01T12:00:00'),
  },
  {
    id: '7',
    content: 'You’re welcome! Glad it helped.',
    postId: '2',
    authorId: '2',
    replyIds: [],
    createdAt: new Date('2024-01-02T12:00:00'),
  },
];

module.exports = { users, posts, comments, categories, tags };
