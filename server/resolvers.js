const { users, posts, comments, categories, tags } = require('./data');

function applyFilters(posts, filter) {
  if (filter.authorId) {
    posts = posts.filter(post => post.authorId === filter.authorId);
  }
  if (filter.categoryId) {
    posts = posts.filter(post => post.categoryId === filter.categoryId);
  }
  if (filter.tagIds) {
    posts = posts.filter(post => filter.tagIds.every(tagId => post.tagIds.includes(tagId)));
  }
  return posts;
}

function applySorting(items, sort) {
  return items.sort((a, b) => {
    if (sort.order === 'ASC') {
      return a[sort.field] > b[sort.field] ? 1 : -1;
    }
    return a[sort.field] < b[sort.field] ? 1 : -1;
  });
}

function applyPagination(items, pagination) {
  if (pagination) {
    const { limit, offset } = pagination;
    return items.slice(offset, offset + limit);
  }
  return items;
}

const resolvers = {
  Query: {
    users: () => users,
    user: (_, { id }) => users.find(user => user.id === id),
    posts: (_, { filter, sort, pagination }) => {
      let result = posts;
      if (filter) {
        result = applyFilters(result, filter);
      }
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
    post: (_, { id }) => posts.find(post => post.id === id),
    comments: (_, { sort, pagination }) => {
      let result = comments;
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
    comment: (_, { id }) => comments.find(comment => comment.id === id),
    categories: () => categories,
    category: (_, { id }) => categories.find(category => category.id === id),
    tags: () => tags,
    tag: (_, { id }) => tags.find(tag => tag.id === id),
  },
  User: {
    friends: (parent) => users.filter(user => parent.friendIds.includes(user.id)),
    posts: (parent) => posts.filter(post => post.authorId === parent.id),
  },
  Category: {
    posts: (parent, { filter, sort, pagination }) => {
      let result = posts.filter(post => post.categoryId === parent.id);
      if (filter) {
        result = applyFilters(result, filter);
      }
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
  },
  Tag: {
    posts: (parent, { filter, sort, pagination }) => {
      let result = posts.filter(post => post.tagIds.includes(parent.id));
      if (filter) {
        result = applyFilters(result, filter);
      }
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
  },
  Post: {
    author: (parent) => users.find(user => user.id === parent.authorId),
    category: (parent) => categories.find(category => category.id === parent.categoryId),
    tags: (parent) => tags.filter(tag => parent.tagIds.includes(tag.id)),
    comments: (parent, { sort, pagination }) => {
      let result = comments.filter(comment => comment.postId === parent.id);
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
  },
  Comment: {
    author: (parent) => users.find(user => user.id === parent.authorId),
    post: (parent) => posts.find(post => post.id === parent.postId),
    replies: (parent, { sort, pagination }) => {
      let result = comments.filter(comment => parent.replyIds.includes(comment.id));
      if (sort) {
        result = applySorting(result, sort);
      }
      if (pagination) {
        result = applyPagination(result, pagination);
      }
      return result;
    },
  },
};

module.exports = resolvers;
