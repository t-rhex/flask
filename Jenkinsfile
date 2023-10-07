pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('docker_hub')
        // Generate a dynamic version based on the current timestamp
        TIMESTAMP = sh(returnStdout: true, script: 'date -u +%Y%m%d%H%M%S').trim()
        DOCKER_IMAGE_VERSION = "v${TIMESTAMP}"
    }
    stages {
        stage('Build') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh "docker build -t trhex/andreew.dev:${DOCKER_IMAGE_VERSION} ."
                }
            }
        }
        stage('Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub', usernameVariable: 'DOCKERHUB_CREDENTIALS_USR', passwordVariable: 'DOCKERHUB_CREDENTIALS_PSW')]) {
                    sh "echo \$DOCKERHUB_CREDENTIALS_PSW | docker login -u \$DOCKERHUB_CREDENTIALS_USR --password-stdin"
                }
            }
        }
        stage('Push') {
            steps {
                sh "docker push trhex/andreew.dev:${DOCKER_IMAGE_VERSION}"
            }
        }
    }
    post {
        always {
            sh 'docker logout'
            // Clean up local Docker images and containers (optional)
            sh 'docker system prune -af'
        }
    }
}
