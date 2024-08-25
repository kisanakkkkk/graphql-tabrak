let users = [
  { id: '1', name: 'John Doe', email: 'john@example.com', age: 30, friendIds: ['2'] },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', age: 25, friendIds: ['1', '3'] },
  { id: '3', name: 'Alice Johnson', email: 'alice@example.com', age: 28, friendIds: ['2'] },
];

let posts = [
  { id: '1', title: 'First Post', content: 'This is the first post', authorId: '1', commentIds: ['1'] },
  { id: '2', title: 'Second Post', content: 'This is another post', authorId: '2', commentIds: ['2'] },
];

let comments = [
  { id: '1', content: 'Great post!', postId: '1', authorId: '2' },
  { id: '2', content: 'Interesting thoughts.', postId: '2', authorId: '1' },
];

module.exports = { users, posts, comments };
