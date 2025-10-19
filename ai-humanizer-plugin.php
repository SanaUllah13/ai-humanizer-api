<?php
/**
 * Plugin Name: AI Text Humanizer
 * Plugin URI: https://github.com/yourusername/ai-humanizer
 * Description: Transforms AI-generated text into natural, academic writing. Use shortcode [ai_humanizer] to embed the tool.
 * Version: 1.0.0
 * Author: Your Name
 * Author URI: https://yourwebsite.com
 * License: MIT
 * Text Domain: ai-humanizer
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Shortcode to display the AI Humanizer interface
 * Usage: [ai_humanizer]
 */
function ai_humanizer_shortcode($atts) {
    // Parse shortcode attributes
    $atts = shortcode_atts(array(
        'api_url' => 'http://localhost:8000', // Default API URL
        'height' => '800px'
    ), $atts);

    // Start output buffering
    ob_start();
    
    // Include the HTML interface
    $html_file = plugin_dir_path(__FILE__) . 'index.html';
    
    if (file_exists($html_file)) {
        // Read the HTML file
        $html_content = file_get_contents($html_file);
        
        // Replace the default API URL with the one from shortcode attribute
        $html_content = str_replace(
            'value="http://localhost:8000"',
            'value="' . esc_attr($atts['api_url']) . '"',
            $html_content
        );
        
        // Output the modified HTML
        echo $html_content;
    } else {
        echo '<div class="error"><p>AI Humanizer: index.html file not found. Please upload it to the plugin directory.</p></div>';
    }
    
    return ob_get_clean();
}

add_shortcode('ai_humanizer', 'ai_humanizer_shortcode');

/**
 * Enqueue scripts and styles (if needed)
 */
function ai_humanizer_enqueue_scripts() {
    // Add any additional scripts or styles here if needed
    // For now, everything is in the HTML file
}

add_action('wp_enqueue_scripts', 'ai_humanizer_enqueue_scripts');

/**
 * Add settings page to WordPress admin (optional)
 */
function ai_humanizer_add_admin_menu() {
    add_options_page(
        'AI Humanizer Settings',
        'AI Humanizer',
        'manage_options',
        'ai-humanizer',
        'ai_humanizer_settings_page'
    );
}

add_action('admin_menu', 'ai_humanizer_add_admin_menu');

/**
 * Settings page content
 */
function ai_humanizer_settings_page() {
    ?>
    <div class="wrap">
        <h1>AI Text Humanizer Settings</h1>
        
        <h2>How to Use</h2>
        <p>Add the following shortcode to any page or post:</p>
        <code>[ai_humanizer]</code>
        
        <h3>Custom API URL</h3>
        <p>To specify a custom API URL:</p>
        <code>[ai_humanizer api_url="https://your-api.com"]</code>
        
        <h3>Installation Checklist</h3>
        <ol>
            <li>✅ Plugin activated</li>
            <li>✓ Upload <code>index.html</code> to the plugin directory</li>
            <li>✓ Deploy backend API (see README.md)</li>
            <li>✓ Update API URL in shortcode</li>
            <li>✓ Add shortcode to a page</li>
        </ol>
        
        <h3>Plugin Files</h3>
        <p>Plugin directory: <code><?php echo plugin_dir_path(__FILE__); ?></code></p>
        <p>Expected files:</p>
        <ul>
            <li><code>ai-humanizer-plugin.php</code> (this file)</li>
            <li><code>index.html</code> (frontend interface)</li>
        </ul>
        
        <h3>Support</h3>
        <p>For help and documentation, visit the <a href="https://github.com/yourusername/ai-humanizer" target="_blank">GitHub repository</a>.</p>
    </div>
    <?php
}
?>
