const { users, posts, comments } = require('./data');

const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(user => user.id === id),
    posts: () => posts,
    post: (_, { id }) => posts.find(post => post.id === id),
    comments: () => comments,
    comment: (_, { id }) => comments.find(comment => comment.id === id),
  },
  User: {
    friends: (parent) => users.filter(user => parent.friendIds.includes(user.id)),
    posts: (parent) => posts.filter(post => post.authorId === parent.id),
  },
  Post: {
    author: (parent) => users.find(user => user.id === parent.authorId),
    comments: (parent) => comments.filter(comment => comment.postId === parent.id),
  },
  Comment: {
    author: (parent) => users.find(user => user.id === parent.authorId),
    post: (parent) => posts.find(post => post.id === parent.postId),
  },
};

module.exports = resolvers;
