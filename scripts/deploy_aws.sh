#!/usr/bin/env bash
set -euo pipefail

export AWS_DEFAULT_REGION=us-east-2
export AWS_PAGER=""

APP="Individual_Assignment_1"
ENV="IndividualAssignment1-env"
BUCKET="elasticbeanstalk-us-east-2-550097745854"

VERSION="travis-${TRAVIS_COMMIT}"
KEY="travis-deployments/${VERSION}.zip"

echo "Packaging application..."
git archive --format=zip --output=/tmp/django-deploy.zip HEAD

echo "Uploading source bundle..."
aws s3 cp /tmp/django-deploy.zip "s3://${BUCKET}/${KEY}"

echo "Checking application version..."
EXISTING_VERSION=$(aws elasticbeanstalk describe-application-versions \
  --application-name "$APP" \
  --version-labels "$VERSION" \
  --query 'ApplicationVersions[0].VersionLabel' \
  --output text)

if [[ "$EXISTING_VERSION" == "$VERSION" ]]; then
  echo "Application version already exists. Reusing it."
else
  echo "Creating application version..."
  aws elasticbeanstalk create-application-version \
    --application-name "$APP" \
    --version-label "$VERSION" \
    --source-bundle S3Bucket="$BUCKET",S3Key="$KEY"
fi

echo "Deploying version: ${VERSION}"
aws elasticbeanstalk update-environment \
  --environment-name "$ENV" \
  --version-label "$VERSION"

echo "Checking deployment completion..."
aws elasticbeanstalk wait environment-updated \
  --environment-names "$ENV"

DEPLOYED_VERSION=$(aws elasticbeanstalk describe-environments \
  --environment-names "$ENV" \
  --query 'Environments[0].VersionLabel' \
  --output text)

if [[ "$DEPLOYED_VERSION" != "$VERSION" ]]; then
  echo "ERROR: Expected ${VERSION}, found ${DEPLOYED_VERSION}"
  exit 1
fi

echo "SUCCESS: Deployed ${VERSION}"
