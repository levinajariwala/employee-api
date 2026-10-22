pipeline {
  agent any

  environment {
    AWS_DEFAULT_REGION = 'eu-west-2'
    AWS_PROFILE        = 'employee-lab'
    APP      = 'employee-api'
    ACCOUNT  = sh(script: 'aws sts get-caller-identity --query Account --output text', returnStdout: true).trim()
    REGISTRY = "${ACCOUNT}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
    IMAGE    = "${REGISTRY}/${APP}"
    CLUSTER  = "${APP}-cluster"
    SERVICE  = "${APP}-service"
  }

  stages {
    stage('Build') {
      steps {
        sh 'echo "Deploying to account $ACCOUNT, image $IMAGE"'
        sh 'docker build --platform linux/amd64 -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
      }
    }
    stage('Test') {
      steps {
        sh 'docker run --rm $IMAGE:latest python -c "import main"'
      }
    }
    stage('Push to ECR') {
      steps {
        sh 'aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY'
        sh 'docker push $IMAGE:$BUILD_NUMBER'
        sh 'docker push $IMAGE:latest'
      }
    }
    stage('Deploy to ECS') {
      steps {
        sh 'aws ecs update-service --cluster $CLUSTER --service $SERVICE --force-new-deployment'
        sh 'aws ecs wait services-stable --cluster $CLUSTER --services $SERVICE'
      }
    }
  }
}