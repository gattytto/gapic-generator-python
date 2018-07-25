# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import textwrap


def wrap(text: str, width: int, initial_width: int = None,
         subsequent_indent: str = '') -> str:
    """Wrap the given string to the given width.

    This uses :meth:`textwrap.fill` under the hood, but provides functionality
    for the initial width, as well as a common line ending for every line
    but the last.

    This is provided to all templates as the ``wrap`` filter.

    Args:
        text (str): The initial text string.
        width (int): The width at which to wrap the text. If either
            ``subsequent_indent`` or ``antecedent_trailer`` are provided,
            their width will be automatically counted against this.
        initial_width (int): Optional. The width of the first line, if
            different. Defaults to the value of ``width``.
        subsequent_indent (str): A string to be prepended to every line
            except the first.

    Returns:
        str: The wrapped string.
    """
    initial_width = initial_width or width

    # Sanity check: If there is empty text, abort.
    if not text:
        return ''

    # Protocol buffers preserves single initial spaces after line breaks
    # when parsing comments (such as the space before the "w" in "when" here).
    # Re-wrapping causes these to be two spaces; correct for this.
    text = text.replace('\n ', '\n')

    # If the initial width is different, break off the beginning of the
    # string.
    first = ''
    if initial_width != width:
        initial = textwrap.wrap(text,
            break_long_words=False,
            width=initial_width,
        )
        first = f'{initial[0]}\n'
        text = ' '.join(initial[1:])

    # Wrap the remainder of the string at the desired width.
    return '{first}{text}'.format(
        first=first,
        text=textwrap.fill(
            break_long_words=False,
            initial_indent=subsequent_indent if first else '',
            subsequent_indent=subsequent_indent,
            text=text,
            width=width,
        ),
    ).rstrip('\n')