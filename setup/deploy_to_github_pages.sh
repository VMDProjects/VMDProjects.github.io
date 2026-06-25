#!/bin/bash
# Auto-deployment for GitHub Pages -- Iran-Optimized Crypto Income Edition
GIT_USER="your-github-username"
GIT_REPO="autocontent-income.github.io"
ARTICLE_DIR="/c/Users/10/.hermes/projects/auto-content-site/content/articles"
DEPLOY_DIR="/tmp/deploy-acg"

rm -rf ${DEPLOY_DIR} && mkdir -p ${DEPLOY_DIR}
cp ${ARTICLE_DIR}/*.html ${DEPLOY_DIR}/ 2>/dev/null || echo "No HTML files"
echo "Ready to push to https://github.com/${GIT_USER}/${GIT_REPO}"
