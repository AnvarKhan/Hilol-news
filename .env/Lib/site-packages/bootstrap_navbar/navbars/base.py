from typing import Union, Optional, Dict, List, Any
from urllib.parse import urlparse, urlencode, urlunparse, ParseResult
from django.template.loader import get_template
from django.template import Engine, Context


class LazyAttribute:
    """Allows for lazy evaluation of some nav item."""

    def __init__(self, method: str) -> None:
        """Initialize the instance with the method name to be
        called.
        """

        self._method = method

    def __call__(self, navgroup: Any, context: Dict) -> Optional[Any]:
        """Call the provided method name on the navgroup."""

        method = getattr(navgroup, self._method)
        return method(context=context)


class Text:
    def __init__(self, template: str) -> None:
        self._engine = Engine()
        self._template = self._engine.from_string(template)

    def render(self, context: Dict) -> str:
        return self._template.render(Context(context=context))


class Href:
    def __init__(self, url: str, query_params: Dict = None) -> None:
        self._url = str(url)
        self._parse_result = urlparse(self._url)
        self._query_params = query_params or {}
        self._query = urlencode(self._query_params)

    def __str__(self) -> str:
        components = (
            self._parse_result.scheme,
            self._parse_result.netloc,
            self._parse_result.path,
            self._parse_result.params,
            self._query,
            self._parse_result.fragment,
        )

        return urlunparse(components)

    def __repr__(self) -> str:
        return str(self)


class NavItemBase:
    """Provides base attributes for navigation items (anchor tags)."""

    template_name = None

    def __init__(
        self,
        *,
        text: Union[Text, str],
        active: bool = False,
        disabled: bool = False,
        active_class: str = "active",
        class_list: List = None,
        attrs: Dict = None,
    ) -> None:
        """Instantiate the class instance."""

        self._text = text
        self._active = active
        self._disabled = disabled
        self._active_class = active_class
        self._class_set = set(class_list or [])
        self._attrs = attrs

        if self.template_name is None:
            raise ValueError("'template_name' template name is a required property")

    @property
    def text(self):
        return self._text

    @property
    def class_list(self) -> List:
        class_list = list(self._class_set)

        if self._active:
            class_list.append(self.active_class)

        return class_list

    @property
    def active_class(self) -> str:
        return self._active_class

    @active_class.setter
    def active_class(self, value: str) -> None:
        self._active_class = value

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        """Set the navitem as active."""

        self._active = value

    @property
    def disabled(self):
        return self._disabled

    @property
    def attrs(self):
        return self._attrs or {}

    def get_context_data(self) -> Dict:
        """Return the default context."""

        return {
            "text": self.text,
            "active": self.active,
            "disabled": self.disabled,
            "active_class": self.active_class,
            "class_list": self.class_list,
            "attrs": self.attrs,
        }

    def render(self) -> str:
        """Render the nav item using the provided template."""

        context = self.get_context_data()
        return get_template(self.template_name).render(context=context)


class NavLinkBase(NavItemBase):
    """Provides base attributes for navigation items (anchor tags)."""

    template_name = None

    def __init__(
        self,
        *,
        text: str,
        href: Union[str, Href] = None,
        active: bool = False,
        disabled: bool = False,
        active_class: str = "active",
        class_list: List = None,
        attrs: Dict = None,
    ) -> None:
        """Instantiate the class instance."""

        super().__init__(
            text=text,
            active=active,
            disabled=disabled,
            active_class=active_class,
            class_list=class_list,
            attrs=attrs,
        )

        self._href = href

    @property
    def url_components(self) -> ParseResult:
        return urlparse(f"{self._href}")

    @property
    def href(self) -> Optional[str]:
        if self._href is None:
            return None

        return str(self._href)

    def get_context_data(self) -> Dict:
        """Return the default context."""

        context = super().get_context_data()
        context.update({"href": self.href})
        return context
