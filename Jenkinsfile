pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('docker_hub')
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build image -t trhex/andreew.dev.0.1.0 .'
      }
    }
    stage('Login') {
      steps {
        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
      }
    }
    stage('Push') {
      steps {
        sh 'docker push trhex/andreew.dev.0.1.0'
      }
    }
  }
  post {
    always {
      sh 'docker logout'
    }
  }
}