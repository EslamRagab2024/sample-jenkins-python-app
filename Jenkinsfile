pipeline {
    agent any

    environment {
        IMAGE_NAME = 'python-hello-world'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from Repository...'
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    script {
                        def fullImageName = "${DOCKER_USER}/${IMAGE_NAME}"
                        echo "Building Docker Image version: ${IMAGE_TAG}..."
                        sh "docker build -t ${fullImageName}:${IMAGE_TAG} -t ${fullImageName}:latest ."
                    }
                }
            }
        }

        stage('Test / Run Container') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    script {
                        def fullImageName = "${DOCKER_USER}/${IMAGE_NAME}"
                        echo "Testing Container output..."
                        sh "docker run --rm ${fullImageName}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                    script {
                        def fullImageName = "${DOCKER_USER}/${IMAGE_NAME}"

                        echo "Logging into Docker Hub and Pushing Image..."
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${fullImageName}:${IMAGE_TAG}"
                        sh "docker push ${fullImageName}:latest"
                    }
                }
            }
        }
    }

    post {
        always {
            withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                script {
                    def fullImageName = "${DOCKER_USER}/${IMAGE_NAME}"
                    echo 'Cleaning up local images and logging out...'
                    sh "docker rmi ${fullImageName}:${IMAGE_TAG} ${fullImageName}:latest || true"
                    sh 'docker logout'
                }
            }
        }
    }
}