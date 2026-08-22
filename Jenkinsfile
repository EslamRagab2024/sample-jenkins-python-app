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
                        echo "Testing Container output via curl..."
                        
                        // 1. تنظيف أي حاوية اختبار قديمة مسجلة بنفس الاسم (تجنباً للتصادم)
                        sh "docker rm -f pipeline-test-app || true"
                        
                        // 2. تشغيل الـ Container في الخلفية على بورت 8000
                        sh "docker run -d -p 8000:8000 --name pipeline-test-app ${fullImageName}:${IMAGE_TAG}"
                        
                        // 3. انتظار ثانيتين للتأكد من استقرار السيرفر
                        sleep 2
                        
                        // 4. اختبار الـ Web Server بطلب curl
                        sh "curl -f http://localhost:8000"
                        
                        // 5. حذف حاوية الاختبار المؤقتة
                        sh "docker rm -f pipeline-test-app"
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
                    sh "docker rm -f pipeline-test-app || true"
                    sh "docker rmi ${fullImageName}:${IMAGE_TAG} ${fullImageName}:latest || true"
                    sh 'docker logout'
                }
            }
        }
    }
}