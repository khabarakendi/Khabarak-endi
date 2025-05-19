<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// Path to archive.json (relative to this PHP file)
$archiveFile = __DIR__ . '/../data/archive.json';

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $input && isset($input['articles'])) {
    try {
        // Read existing archive
        $existing = [];
        if (file_exists($archiveFile)) {
            $existing = json_decode(file_get_contents($archiveFile), true) ?: [];
        }

        // Merge and deduplicate
        $urls = array_column($existing, 'url');
        $newArticles = array_filter($input['articles'], function($article) use ($urls) {
            return !in_array($article['url'], $urls);
        });

        // Combine and limit to 500 most recent
        $updatedArchive = array_merge($newArticles, $existing);
        $updatedArchive = array_slice($updatedArchive, 0, 500);

        // Save to file
        file_put_contents($archiveFile, json_encode($updatedArchive, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        echo json_encode(['success' => true, 'count' => count($updatedArchive)]);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
    }
} else {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Invalid request']);
}
