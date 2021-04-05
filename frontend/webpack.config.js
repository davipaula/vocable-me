module.exports = {
  devServer: {
    proxy: {
      '/api': 'http://localhost',
    },
  },
};
