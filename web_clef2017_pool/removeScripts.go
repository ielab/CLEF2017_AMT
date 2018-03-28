// Thanks to peterSO: https://codereview.stackexchange.com/questions/161461/golang-function-to-clean-a-string-of-scripts

package main


import "strings"

// removeScripts removes all HTML script elements.
func removeScripts(s string) string {
	const (
		startTag = "<script"
		endTag   = "</script>"
	)

	start := strings.Index(s, startTag)
	if start < 0 {
		return s
	}

	b := make([]byte, start, len(s))
	copy(b, s)

	for {
		end := strings.Index(s[start+len(startTag):], endTag)
		if end < 0 {
			b = append(b, s[start:]...)
			break
		}
		end += (start + len(startTag)) + len(endTag)

		start = strings.Index(s[end:], startTag)
		if start < 0 {
			b = append(b, s[end:]...)
			break
		}
		start += end

		b = append(b, s[end:start]...)
	}

	return string(b)
}

