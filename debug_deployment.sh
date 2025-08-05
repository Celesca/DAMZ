#!/bin/bash

echo "🔍 Checking Docker Compose Status..."
echo "=================================="

# Check if containers are running
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🔍 Checking team06-grounding-dino logs:"
echo "======================================="
docker logs team06-grounding-dino --tail 50

echo ""
echo "🔍 Checking if containers are healthy:"
echo "====================================="
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🔍 Testing API endpoint (if running):"
echo "===================================="
curl -f http://localhost:1600/health 2>/dev/null && echo "✅ API is responding" || echo "❌ API is not responding"

echo ""
echo "🔍 Checking video action status:"
echo "==============================="
curl -f http://localhost:1600/video_action/status 2>/dev/null && echo "✅ Video action endpoint responding" || echo "❌ Video action endpoint not responding"

echo ""
echo "📝 Quick Debugging Commands:"
echo "============================"
echo "docker logs team06-grounding-dino --follow"
echo "docker exec -it team06-grounding-dino /bin/bash"
echo "docker-compose down && docker-compose up --build -d"
