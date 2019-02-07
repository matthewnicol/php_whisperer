<?php
 class Node {
 public $value, $left, $right;
 public function __construct($value) {
    $this->value = $value;
 }
 }

 class BST {
 public $root;
 public function __construct($items) {
    foreach ($items as $item) {
        $this->insert($item);
    }
 }
 public function search($value) {
 $node = $this->root;
 while ($node) {
    if ($value > $node->value) {
        $node = $node->right;
    } else if ($value < $node->value) {
        $node = $node->left;
    }
    else {
        $break;
    }

 }
 return $node;

 }

 public function insert($value) {
    $node = $this->root;
    if (!$node) {
        $this->root = new Node($value);
    }

    while ($node) {
        if ($value > $node->value) {
            if ($node->right) {
                $node = $node->right;
            } else {
                $node->right = new Node($value);
                return;
            }
        } else if ($value < $node->value) {
            if ($node->left) {
                $node = $node->left;
            } else {
                $node->left = new Node($value);
                return;
            }

        }
        else {
            return;
        }

            }
        }

    public function find($value) {
        $node = $this->root;
        if (!$node) { return false; }
        while ($node) {
            if ($value == $node->value) {
            return true;
            }
            else if ($value < $node->value) {
            $node = $node->left;
            }
            else if ($value > $node->value) {
            $node = $node->right;
            }
        }
        return false;
    }
 }

 $bst = new BST($builtins);


